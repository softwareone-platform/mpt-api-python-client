## Add repo-specific targets here. Do not modify the shared *.mk files.
e2e:  ## Run e2e test
	$(RUN) pytest -p no:randomly --junitxml=e2e-report.xml $(if $(args),$(args), tests/e2e)
