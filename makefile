all:
	@echo "Digite make run para executar o programa"
	@echo "Digite make clean para limpar os arquivos gerados"
	@echo "Digite make clean_tables para limpar as tabelas de input"

run:
	@python3 src/comparator.py > Results/log.md
	@cat Results/log.md

clean:
	@rm -rf Results/*.xlsx
	@> Results/log.md

clean_tables:
	@rm -rf tables/*.xlsx

