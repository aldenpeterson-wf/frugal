package test

import (
	"bufio"
	"os"
	"testing"
)

const (
	outputDir               = "out"
	delim                   = "."
	validFile               = "idl/valid.frugal"
	invalidFile             = "idl/invalid.frugal"
	duplicateServices       = "idl/duplicate_services.frugal"
	duplicateScopes         = "idl/duplicate_scopes.frugal"
	duplicateMethods        = "idl/duplicate_methods.frugal"
	duplicateOperations     = "idl/duplicate_operations.frugal"
	duplicateMethodArgIds   = "idl/duplicate_arg_ids.frugal"
	duplicateStructFieldIds = "idl/duplicate_field_ids.frugal"
	frugalGenFile           = "idl/variety.frugal"
	badNamespace            = "idl/bad_namespace.frugal"
	includeVendor           = "idl/include_vendor.frugal"
	includeVendorNoPath     = "idl/include_vendor_no_path.frugal"
	vendorNamespace         = "idl/vendor_namespace.frugal"
)

func compareFiles(t *testing.T, expectedPath, generatedPath string) {
	expected, err := os.Open(expectedPath)
	if err != nil {
		t.Fatalf("Failed to open file %s", expectedPath)
	}
	defer expected.Close()
	generated, err := os.Open(generatedPath)
	if err != nil {
		t.Fatalf("Failed to open file %s", generatedPath)
	}
	defer generated.Close()

	expectedScanner := bufio.NewScanner(expected)
	generatedScanner := bufio.NewScanner(generated)
	line := 1
	for expectedScanner.Scan() {
		generatedScanner.Scan()
		expectedLine := expectedScanner.Text()
		generatedLine := generatedScanner.Text()
		if expectedLine != generatedLine {
			t.Fatalf("Expected line <%s> (%s)\n, generated line <%s> (%s)\n at line %d",
				expectedLine, expectedPath, generatedLine, generatedPath, line)
		}
		line++
	}

	if generatedScanner.Scan() {
		t.Fatalf("Generated has more lines than expected: exp %s gen %s", expectedPath, generatedPath)
	}
}
