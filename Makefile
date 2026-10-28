.PHONY: clean_venv

clean_venv:
	@find -type d -name "*.venv" -exec rm -r {} +
	@printf "Success\n"