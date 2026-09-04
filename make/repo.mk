## Add repo-specific targets here. Do not modify the shared *.mk files.
e2e:  ## Run e2e test. Pass args=<options> for extra pytest options, path=<target> to narrow the tests
	$(RUN) pytest -p no:randomly --junitxml=e2e-report.xml $(args) $(if $(path),$(path),tests/e2e)
