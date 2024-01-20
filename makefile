all:
	@echo "Digite make run para executar o programa"
	@echo "Digite make clean para limpar os arquivos gerados"
	@echo "Digite make clean_tables para limpar as tabelas de input"

run:
	@python3 src/comparator.py > Results/log.txt
	@cat Results/log.txt

clean:
	@rm -rf Results/*.xlsx
	@> Results/log.txt
	@touch Results/log.txt

clean_tables:
	@rm -rf tables/*.xlsx

