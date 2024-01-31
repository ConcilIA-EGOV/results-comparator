all:
	@echo "Digite make run para executar o programa"
	@echo "Digite make clean para limpar os arquivos gerados"
	@echo "Digite make clean_tables para limpar as tabelas de input"

run:
	@python3 src/comparator.py > Resultados/log.txt
	@cat Resultados/log.txt

clean:
	@rm -rf Resultados/*.xlsx
	@rm -rf Resultados/*.txt

clean_tables:
	@rm -rf tables/*.xlsx

