all:
	@echo "Digite make run para executar o programa"
	@echo "Digite make clean para limpar os arquivos gerados"
	@echo "Digite make clean_tables para limpar as tabelas de input"
	@echo "Digite make formating para formatar as variáveis"

run:
	@python3 src/comparator.py

clean:
	@rm -rf Resultados/*/
	@rm -rf Resultados/*.xlsx
	@rm -rf Resultados/*.txt
	@rm -rf Resultados/*.csv

clean_tables:
	@rm -rf tables/*/*.csv

make formating:
	@python3 src/variable_formatation.py
