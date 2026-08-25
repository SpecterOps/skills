// Command go_inventory builds a conservative, AST-backed Go source inventory
// for the go-review security review skill.
package main

import (
	"bufio"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"io/fs"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
)

var ignoredDirs = map[string]bool{
	".git":               true,
	"vendor":             true,
	"node_modules":       true,
	".go-review-results": true,
}

var serviceImports = map[string]string{
	"net/http":                 "net/http",
	"google.golang.org/grpc":   "grpc",
	"github.com/gin-gonic/gin": "gin",
	"github.com/labstack/echo": "echo",
	"github.com/go-chi/chi":    "chi",
	"github.com/gofiber/fiber": "fiber",
	"github.com/gorilla/mux":   "gorilla/mux",
}

var sqlImportPrefixes = []string{
	"database/sql",
	"github.com/jmoiron/sqlx",
	"github.com/jackc/pgx",
	"gorm.io/gorm",
	"entgo.io/ent",
}

var cryptoAuthImportPrefixes = []string{
	"crypto/",
	"golang.org/x/crypto",
	"github.com/golang-jwt/jwt",
	"github.com/dgrijalva/jwt-go",
	"github.com/gorilla/sessions",
}

type functionRecord struct {
	Name     string  `json:"name"`
	Receiver *string `json:"receiver"`
	Exported bool    `json:"exported"`
	Line     int     `json:"line"`
}

type fileRecord struct {
	Path      string           `json:"path"`
	Package   string           `json:"package"`
	Imports   []string         `json:"imports"`
	Functions []functionRecord `json:"functions"`
	Routes    []map[string]any `json:"routes"`
}

type capabilityFlags struct {
	HasService      bool `json:"has_service"`
	HasOutboundHTTP bool `json:"has_outbound_http"`
	HasSQL          bool `json:"has_sql"`
	HasExec         bool `json:"has_exec"`
	HasFSArchive    bool `json:"has_fs_archive"`
	HasTemplate     bool `json:"has_template"`
	HasCryptoAuth   bool `json:"has_crypto_auth"`
	HasConcurrency  bool `json:"has_concurrency"`
	HasUnsafeCgo    bool `json:"has_unsafe_cgo"`
}

type summary struct {
	GoFileCount     int `json:"go_file_count"`
	PackageCount    int `json:"package_count"`
	EntrypointCount int `json:"entrypoint_count"`
	FrameworkCount  int `json:"framework_count"`
}

type inventory struct {
	Version         int              `json:"version"`
	RepoRoot        string           `json:"repo_root"`
	ScopeSubpath    string           `json:"scope_subpath"`
	Module          *string          `json:"module"`
	Files           []fileRecord     `json:"files"`
	Frameworks      []string         `json:"frameworks"`
	Entrypoints     []map[string]any `json:"entrypoints"`
	CapabilityFlags capabilityFlags  `json:"capability_flags"`
	Summary         summary          `json:"summary"`
}

type callFact struct {
	PackagePath string
	Name        string
}

type fileFacts struct {
	Imports     []string
	Calls       []callFact
	Identifiers map[string]bool
	HasGoStmt   bool
	HasChanType bool
}

func canonicalPath(path string) (string, error) {
	abs, err := filepath.Abs(path)
	if err != nil {
		return "", err
	}
	resolved, err := filepath.EvalSymlinks(abs)
	if err != nil {
		return "", err
	}
	return filepath.Clean(resolved), nil
}

func portablePath(path string) string {
	return strings.ReplaceAll(filepath.ToSlash(path), `\`, "/")
}

func isWithin(root, candidate string) bool {
	rel, err := filepath.Rel(root, candidate)
	if err != nil {
		return false
	}
	return rel != ".." && !strings.HasPrefix(rel, ".."+string(filepath.Separator))
}

func discoverGoFiles(repoRoot, scopeSubpath string) ([]string, error) {
	scopeInput := filepath.Join(repoRoot, scopeSubpath)
	info, err := os.Stat(scopeInput)
	if errors.Is(err, fs.ErrNotExist) {
		return []string{}, nil
	}
	if err != nil {
		return nil, err
	}
	scope, err := canonicalPath(scopeInput)
	if err != nil {
		return nil, err
	}
	if !isWithin(repoRoot, scope) {
		return []string{}, nil
	}

	include := func(path string) bool {
		if filepath.Ext(path) != ".go" || strings.HasSuffix(path, "_test.go") {
			return false
		}
		rel, err := filepath.Rel(repoRoot, path)
		if err != nil || !isWithin(repoRoot, path) {
			return false
		}
		for _, part := range strings.Split(portablePath(rel), "/") {
			if ignoredDirs[part] {
				return false
			}
		}
		return true
	}

	if !info.IsDir() {
		if include(scope) {
			return []string{scope}, nil
		}
		return []string{}, nil
	}

	var files []string
	err = filepath.WalkDir(scope, func(path string, entry fs.DirEntry, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		if entry.IsDir() && path != scope && ignoredDirs[entry.Name()] {
			return filepath.SkipDir
		}
		if !entry.IsDir() && include(path) {
			files = append(files, path)
		}
		return nil
	})
	if err != nil {
		return nil, err
	}
	sort.Strings(files)
	return files, nil
}

func readModule(repoRoot string) (*string, error) {
	file, err := os.Open(filepath.Join(repoRoot, "go.mod"))
	if errors.Is(err, fs.ErrNotExist) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())
		if len(fields) < 2 || fields[0] != "module" {
			continue
		}
		value := fields[1]
		if unquoted, err := strconv.Unquote(value); err == nil {
			value = unquoted
		}
		return &value, nil
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}
	return nil, nil
}

func importName(path string) string {
	parts := strings.Split(path, "/")
	last := parts[len(parts)-1]
	if len(parts) > 1 && len(last) > 1 && last[0] == 'v' {
		if _, err := strconv.Atoi(last[1:]); err == nil {
			return parts[len(parts)-2]
		}
	}
	return last
}

func receiverText(fset *token.FileSet, receiver *ast.FieldList, source []byte) (*string, error) {
	if receiver == nil {
		return nil, nil
	}
	file := fset.File(receiver.Pos())
	if file == nil {
		return nil, errors.New("receiver has no token file")
	}
	start := file.Offset(receiver.Opening)
	end := file.Offset(receiver.Closing) + 1
	if start < 0 || end > len(source) || start >= end {
		return nil, errors.New("receiver has invalid source positions")
	}
	text := string(source[start:end])
	return &text, nil
}

func stringArgument(call *ast.CallExpr, index int) (string, bool) {
	if index >= len(call.Args) {
		return "", false
	}
	literal, ok := call.Args[index].(*ast.BasicLit)
	if !ok || literal.Kind != token.STRING {
		return "", false
	}
	value, err := strconv.Unquote(literal.Value)
	return value, err == nil
}

func callNameAndRoot(call *ast.CallExpr) (name, root string) {
	switch fun := call.Fun.(type) {
	case *ast.Ident:
		return fun.Name, ""
	case *ast.SelectorExpr:
		name = fun.Sel.Name
		current := fun.X
		for {
			switch node := current.(type) {
			case *ast.Ident:
				return name, node.Name
			case *ast.SelectorExpr:
				current = node.X
			default:
				return name, ""
			}
		}
	default:
		return "", ""
	}
}

func routeForCall(call *ast.CallExpr, fset *token.FileSet) map[string]any {
	name, _ := callNameAndRoot(call)
	line := fset.Position(call.Pos()).Line
	path, hasPath := stringArgument(call, 0)

	switch name {
	case "HandleFunc", "Handle":
		if hasPath {
			return map[string]any{"kind": name, "method": nil, "path": path, "line": line}
		}
	case "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD":
		if hasPath {
			return map[string]any{"kind": "router-method", "method": name, "path": path, "line": line}
		}
	case "MethodFunc":
		if hasPath {
			return map[string]any{"kind": "router-handle", "method": nil, "path": path, "line": line}
		}
	}

	if strings.HasPrefix(name, "Register") && strings.HasSuffix(name, "Server") {
		service := strings.TrimSuffix(strings.TrimPrefix(name, "Register"), "Server")
		if service != "" {
			return map[string]any{"kind": "grpc-register", "service": service, "line": line}
		}
	}
	return nil
}

func analyzeFile(path, repoRoot string) (fileRecord, fileFacts, error) {
	source, err := os.ReadFile(path)
	if err != nil {
		return fileRecord{}, fileFacts{}, err
	}
	fset := token.NewFileSet()
	parsed, err := parser.ParseFile(fset, path, source, parser.ParseComments|parser.AllErrors)
	if err != nil {
		return fileRecord{}, fileFacts{}, fmt.Errorf("parse %s: %w", path, err)
	}

	aliases := make(map[string]string)
	imports := make([]string, 0, len(parsed.Imports))
	for _, spec := range parsed.Imports {
		importPath, err := strconv.Unquote(spec.Path.Value)
		if err != nil {
			return fileRecord{}, fileFacts{}, fmt.Errorf("parse import in %s: %w", path, err)
		}
		imports = append(imports, importPath)
		name := importName(importPath)
		if spec.Name != nil {
			name = spec.Name.Name
		}
		if name != "_" && name != "." {
			aliases[name] = importPath
		}
	}
	sort.Strings(imports)
	imports = compactStrings(imports)

	functions := make([]functionRecord, 0)
	for _, declaration := range parsed.Decls {
		function, ok := declaration.(*ast.FuncDecl)
		if !ok {
			continue
		}
		receiver, err := receiverText(fset, function.Recv, source)
		if err != nil {
			return fileRecord{}, fileFacts{}, err
		}
		functions = append(functions, functionRecord{
			Name:     function.Name.Name,
			Receiver: receiver,
			Exported: ast.IsExported(function.Name.Name),
			Line:     fset.Position(function.Pos()).Line,
		})
	}

	routes := make([]map[string]any, 0)
	facts := fileFacts{Imports: imports, Identifiers: make(map[string]bool)}
	ast.Inspect(parsed, func(node ast.Node) bool {
		switch value := node.(type) {
		case *ast.Ident:
			facts.Identifiers[value.Name] = true
		case *ast.GoStmt:
			facts.HasGoStmt = true
		case *ast.ChanType:
			facts.HasChanType = true
		case *ast.CallExpr:
			name, root := callNameAndRoot(value)
			facts.Calls = append(facts.Calls, callFact{PackagePath: aliases[root], Name: name})
			if route := routeForCall(value, fset); route != nil {
				routes = append(routes, route)
			}
		}
		return true
	})

	relative, err := filepath.Rel(repoRoot, path)
	if err != nil {
		return fileRecord{}, fileFacts{}, err
	}
	record := fileRecord{
		Path:      portablePath(relative),
		Package:   parsed.Name.Name,
		Imports:   imports,
		Functions: functions,
		Routes:    routes,
	}
	return record, facts, nil
}

func compactStrings(values []string) []string {
	if len(values) < 2 {
		return values
	}
	result := values[:1]
	for _, value := range values[1:] {
		if value != result[len(result)-1] {
			result = append(result, value)
		}
	}
	return result
}

func hasImportPrefix(imports map[string]bool, prefixes []string) bool {
	for imported := range imports {
		for _, prefix := range prefixes {
			if strings.HasPrefix(imported, prefix) {
				return true
			}
		}
	}
	return false
}

func hasCall(calls []callFact, packagePaths map[string]bool, names map[string]bool) bool {
	for _, call := range calls {
		if names[call.Name] && (packagePaths == nil || packagePaths[call.PackagePath]) {
			return true
		}
	}
	return false
}

func deriveCapabilityFlags(facts []fileFacts, routes []map[string]any) capabilityFlags {
	imports := make(map[string]bool)
	identifiers := make(map[string]bool)
	var calls []callFact
	var hasGoStmt, hasChanType bool
	for _, fact := range facts {
		for _, imported := range fact.Imports {
			imports[imported] = true
		}
		for name := range fact.Identifiers {
			identifiers[name] = true
		}
		calls = append(calls, fact.Calls...)
		hasGoStmt = hasGoStmt || fact.HasGoStmt
		hasChanType = hasChanType || fact.HasChanType
	}

	hasServiceImport := false
	for imported := range serviceImports {
		hasServiceImport = hasServiceImport || imports[imported]
	}
	servicePackages := map[string]bool{"net/http": true, "google.golang.org/grpc": true}
	hasServiceCall := hasCall(calls, servicePackages, map[string]bool{
		"Handle": true, "HandleFunc": true, "ListenAndServe": true, "Serve": true, "NewServer": true,
	})

	hasOutboundHTTP := hasCall(calls, map[string]bool{"net/http": true}, map[string]bool{
		"Get": true, "Post": true, "PostForm": true, "Head": true,
		"NewRequest": true, "NewRequestWithContext": true,
	}) || hasCall(calls, nil, map[string]bool{"Do": true, "RoundTrip": true})

	// Generic receiver methods such as Context.Query are common in frameworks.
	// Require a known database/ORM import to avoid activating SQL review solely
	// because an unrelated type uses a SQL-like method name.
	hasSQL := hasImportPrefix(imports, sqlImportPrefixes)
	hasExec := imports["os/exec"] || hasCall(calls, map[string]bool{"os/exec": true}, map[string]bool{
		"Command": true, "CommandContext": true,
	})
	hasFSArchive := imports["archive/zip"] || imports["archive/tar"] ||
		hasCall(calls, map[string]bool{"os": true, "io/ioutil": true}, map[string]bool{
			"Open": true, "OpenFile": true, "Create": true, "ReadFile": true,
			"WriteFile": true, "Mkdir": true, "MkdirAll": true, "TempFile": true,
			"CreateTemp": true, "Rename": true,
		}) || hasCall(calls, map[string]bool{"path/filepath": true}, map[string]bool{
		"Join": true, "Clean": true, "Walk": true, "WalkDir": true, "Abs": true, "Rel": true,
	})
	hasTemplate := imports["html/template"] || imports["text/template"] ||
		hasCall(calls, nil, map[string]bool{"Execute": true, "ExecuteTemplate": true})
	hasCryptoAuth := hasImportPrefix(imports, cryptoAuthImportPrefixes) || imports["math/rand"] ||
		identifiers["Cookie"] || identifiers["SameSite"] || identifiers["InsecureSkipVerify"]
	hasConcurrency := imports["sync"] || imports["sync/atomic"] || hasGoStmt || hasChanType
	hasUnsafeCgo := imports["unsafe"] || imports["C"]

	return capabilityFlags{
		HasService:      hasServiceImport || hasServiceCall || len(routes) > 0,
		HasOutboundHTTP: hasOutboundHTTP,
		HasSQL:          hasSQL,
		HasExec:         hasExec,
		HasFSArchive:    hasFSArchive,
		HasTemplate:     hasTemplate,
		HasCryptoAuth:   hasCryptoAuth,
		HasConcurrency:  hasConcurrency,
		HasUnsafeCgo:    hasUnsafeCgo,
	}
}

func buildInventory(repoRoot, scopeSubpath string) (inventory, error) {
	root, err := canonicalPath(repoRoot)
	if err != nil {
		return inventory{}, err
	}
	paths, err := discoverGoFiles(root, scopeSubpath)
	if err != nil {
		return inventory{}, err
	}
	module, err := readModule(root)
	if err != nil {
		return inventory{}, err
	}

	files := make([]fileRecord, 0, len(paths))
	allFacts := make([]fileFacts, 0, len(paths))
	frameworkSet := make(map[string]bool)
	packageSet := make(map[string]bool)
	entrypoints := make([]map[string]any, 0)
	for _, path := range paths {
		record, facts, err := analyzeFile(path, root)
		if err != nil {
			return inventory{}, err
		}
		files = append(files, record)
		allFacts = append(allFacts, facts)
		packageSet[record.Package] = true
		for _, imported := range record.Imports {
			if framework, ok := serviceImports[imported]; ok {
				frameworkSet[framework] = true
			}
		}
		for _, route := range record.Routes {
			entrypoint := map[string]any{"file": record.Path}
			for key, value := range route {
				entrypoint[key] = value
			}
			entrypoints = append(entrypoints, entrypoint)
		}
	}

	frameworks := make([]string, 0, len(frameworkSet))
	for framework := range frameworkSet {
		frameworks = append(frameworks, framework)
	}
	sort.Strings(frameworks)
	flags := deriveCapabilityFlags(allFacts, entrypoints)
	return inventory{
		Version:         1,
		RepoRoot:        root,
		ScopeSubpath:    scopeSubpath,
		Module:          module,
		Files:           files,
		Frameworks:      frameworks,
		Entrypoints:     entrypoints,
		CapabilityFlags: flags,
		Summary: summary{
			GoFileCount:     len(files),
			PackageCount:    len(packageSet),
			EntrypointCount: len(entrypoints),
			FrameworkCount:  len(frameworks),
		},
	}, nil
}

func run(args []string) error {
	flags := flag.NewFlagSet("go_inventory", flag.ContinueOnError)
	flags.SetOutput(os.Stderr)
	repoRoot := flags.String("repo-root", "", "repository root (required)")
	scopeSubpath := flags.String("scope-subpath", ".", "path within the repository to inspect")
	output := flags.String("output", "", "inventory JSON output path (required)")
	if err := flags.Parse(args); err != nil {
		return err
	}
	if *repoRoot == "" || *output == "" {
		return errors.New("--repo-root and --output are required")
	}

	result, err := buildInventory(*repoRoot, *scopeSubpath)
	if err != nil {
		return err
	}
	encoded, err := json.MarshalIndent(result, "", "  ")
	if err != nil {
		return err
	}
	if err := os.MkdirAll(filepath.Dir(*output), 0o755); err != nil {
		return err
	}
	if err := os.WriteFile(*output, append(encoded, '\n'), 0o644); err != nil {
		return err
	}
	summaryJSON, err := json.Marshal(result.Summary)
	if err != nil {
		return err
	}
	fmt.Println(string(summaryJSON))
	return nil
}

func main() {
	if err := run(os.Args[1:]); err != nil {
		fmt.Fprintf(os.Stderr, "go_inventory: %v\n", err)
		os.Exit(2)
	}
}
