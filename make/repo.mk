## Add repo-specific targets here. Do not modify the shared *.mk files.
e2e:  ## Run e2e test
	$(RUN) pytest -p no:randomly --no-cov --junitxml=e2e-report.xml $(or $(path),tests/e2e) $(args)
