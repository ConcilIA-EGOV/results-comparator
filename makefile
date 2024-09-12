all:
	@echo "Digite make run para executar o programa"
	@echo "Digite make clean para limpar os arquivos gerados"
	@echo "Digite make clean_tables para limpar as tabelas de input"
	@echo "Digite make formating para formatar as variáveis"

run:
	@python3 src/comparator.py > Resultados/log_comparacao.txt
	@cat Resultados/log_comparacao.txt

clean:
	@rm -rf Resultados/*.xlsx
	@rm -rf Resultados/*.txt

clean_tables:
	@rm -rf tables/*.csv

make formating:
	@python3 src/variable_formatation.py
