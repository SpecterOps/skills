package main

import (
	"os"
	"path/filepath"
	"testing"
)

func writeFixture(t *testing.T, root, name, contents string) {
	t.Helper()
	path := filepath.Join(root, name)
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(path, []byte(contents), 0o644); err != nil {
		t.Fatal(err)
	}
}

func TestBuildInventoryUsesGoSyntax(t *testing.T) {
	root := t.TempDir()
	writeFixture(t, root, "go.mod", "module example.com/service\n\ngo 1.22\n")
	writeFixture(t, root, "cmd/api/main.go", `package main

import (
	"context"
	"database/sql"
	web "net/http"
	"os/exec"
	"sync"

	"google.golang.org/grpc"
)

type server struct{}

func (s *server) ServeHTTP(
	w web.ResponseWriter,
	r *web.Request,
) {
	web.HandleFunc("/healthz", func(web.ResponseWriter, *web.Request) {})
	router.GET("/users", s.users)
	pb.RegisterGreeterServer(grpc.NewServer(), s)
	request, _ := web.NewRequestWithContext(context.Background(), web.MethodGet, "https://example.test", nil)
	_, _ = web.DefaultClient.Do(request)
	_, _ = db.QueryContext(context.Background(), "select 1")
	_ = exec.CommandContext(context.Background(), "echo", "ok")
	go func() {}()
	_ = make(chan struct{})
	_ = sync.Mutex{}
}

func (s *server) users(w web.ResponseWriter, r *web.Request) {}

var db *sql.DB
var router interface{ GET(string, ...any) }
var pb interface{ RegisterGreeterServer(...any) }
`)

	result, err := buildInventory(root, ".")
	if err != nil {
		t.Fatal(err)
	}
	if result.Module == nil || *result.Module != "example.com/service" {
		t.Fatalf("unexpected module: %#v", result.Module)
	}
	if result.Summary.GoFileCount != 1 || result.Summary.EntrypointCount != 3 {
		t.Fatalf("unexpected summary: %#v", result.Summary)
	}
	if len(result.Frameworks) != 2 || result.Frameworks[0] != "grpc" || result.Frameworks[1] != "net/http" {
		t.Fatalf("unexpected frameworks: %#v", result.Frameworks)
	}
	flags := result.CapabilityFlags
	if !flags.HasService || !flags.HasOutboundHTTP || !flags.HasSQL || !flags.HasExec || !flags.HasConcurrency {
		t.Fatalf("expected service capabilities, got %#v", flags)
	}
	functions := result.Files[0].Functions
	if len(functions) != 2 || functions[0].Receiver == nil || *functions[0].Receiver != "(s *server)" {
		t.Fatalf("unexpected functions: %#v", functions)
	}
	if result.Entrypoints[0]["path"] != "/healthz" || result.Entrypoints[1]["method"] != "GET" || result.Entrypoints[2]["service"] != "Greeter" {
		t.Fatalf("unexpected entrypoints: %#v", result.Entrypoints)
	}
}

func TestCommentsAndStringsDoNotCreateCapabilities(t *testing.T) {
	root := t.TempDir()
	writeFixture(t, root, "go.mod", "module example.com/quiet\n")
	writeFixture(t, root, "quiet.go", `package quiet

const decoys = "http.HandleFunc exec.Command db.Query go make(chan string)"

// router.GET("/not-a-route", handler)
func helper() {}
`)

	result, err := buildInventory(root, ".")
	if err != nil {
		t.Fatal(err)
	}
	if result.Summary.EntrypointCount != 0 {
		t.Fatalf("unexpected entrypoints: %#v", result.Entrypoints)
	}
	if result.CapabilityFlags != (capabilityFlags{}) {
		t.Fatalf("decoys produced capability flags: %#v", result.CapabilityFlags)
	}
}

func TestDocumentedBeforeAfterExample(t *testing.T) {
	root := t.TempDir()
	source := "package main\n\n" +
		"import web \"net/http\"\n\n" +
		"func main() {\n" +
		"\tconst documentationExample = `\n" +
		"db.Query(\"SELECT secret FROM users\")\n" +
		"exec.Command(\"sh\", \"-c\", input)\n" +
		"go background()\n" +
		"`\n" +
		"\t_ = documentationExample\n" +
		"\trequest, _ := web.\n" +
		"\t\tNewRequest(\"GET\", \"https://example.test/health\", nil)\n" +
		"\t_ = request\n" +
		"\tweb.HandleFunc(`/healthz`, health)\n" +
		"}\n\n" +
		"func health(web.ResponseWriter, *web.Request) {}\n"
	writeFixture(t, root, "main.go", source)

	result, err := buildInventory(root, ".")
	if err != nil {
		t.Fatal(err)
	}
	flags := result.CapabilityFlags
	if !flags.HasService || !flags.HasOutboundHTTP {
		t.Fatalf("expected real HTTP capabilities, got %#v", flags)
	}
	if flags.HasSQL || flags.HasExec || flags.HasConcurrency {
		t.Fatalf("documentation text produced capabilities: %#v", flags)
	}
	if result.Summary.EntrypointCount != 1 || result.Entrypoints[0]["path"] != "/healthz" {
		t.Fatalf("unexpected entrypoints: %#v", result.Entrypoints)
	}
}

func TestDiscoveryHonorsScopeAndIgnoredPaths(t *testing.T) {
	root := t.TempDir()
	writeFixture(t, root, "service/main.go", "package service\n")
	writeFixture(t, root, "service/main_test.go", "package service\n")
	writeFixture(t, root, "service/vendor/dep.go", "package vendor\n")
	writeFixture(t, root, ".go-review-results/generated.go", "package generated\n")

	result, err := buildInventory(root, "service")
	if err != nil {
		t.Fatal(err)
	}
	if result.Summary.GoFileCount != 1 || result.Files[0].Path != "service/main.go" {
		t.Fatalf("unexpected files: %#v", result.Files)
	}

	outside, err := buildInventory(root, "../outside")
	if err != nil {
		t.Fatal(err)
	}
	if outside.Summary.GoFileCount != 0 {
		t.Fatalf("scope escaped repository: %#v", outside.Files)
	}
}

func TestInvalidGoFailsClosed(t *testing.T) {
	root := t.TempDir()
	writeFixture(t, root, "broken.go", "package broken\nfunc nope(\n")
	if _, err := buildInventory(root, "."); err == nil {
		t.Fatal("expected parser error")
	}
}

func TestFrameworkQueryMethodDoesNotImplySQL(t *testing.T) {
	root := t.TempDir()
	writeFixture(t, root, "context.go", `package framework

type Context struct{}
func (*Context) Query(string) string { return "" }
`)
	result, err := buildInventory(root, ".")
	if err != nil {
		t.Fatal(err)
	}
	if result.CapabilityFlags.HasSQL {
		t.Fatal("an unrelated Query method activated SQL review")
	}
}

func TestBuildTaggedAndNestedModuleFilesAreInventoried(t *testing.T) {
	root := t.TempDir()
	writeFixture(t, root, "go.mod", "module example.com/root\n")
	writeFixture(t, root, "platform_linux.go", "//go:build linux\n\npackage root\n")
	writeFixture(t, root, "nested/go.mod", "module example.com/nested\n")
	writeFixture(t, root, "nested/library.go", "package nested\n")
	result, err := buildInventory(root, ".")
	if err != nil {
		t.Fatal(err)
	}
	if result.Summary.GoFileCount != 2 {
		t.Fatalf("expected an all-platform inventory across nested modules: %#v", result.Files)
	}
	if result.Module == nil || *result.Module != "example.com/root" {
		t.Fatalf("inventory module should identify the review root: %#v", result.Module)
	}
}

func TestPortablePathNormalizesWindowsSeparators(t *testing.T) {
	if got := portablePath(`nested\pkg\file.go`); got != "nested/pkg/file.go" {
		t.Fatalf("unexpected portable path: %q", got)
	}
}
