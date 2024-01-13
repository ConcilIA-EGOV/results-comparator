all:
	@echo "Digite make run para executar o programa"
	@echo "Digite make clean para limpar os arquivos gerados"
	@echo "Digite make clean_tables para limpar as tabelas de input"

run:
	@touch Results/log.txt
	@python3 src/comparator.py > Results/log.txt
	@cat Results/log.txt

clean:
	@rm -rf Results/*
	@echo "!!! não esqueça de apagar as tabelas manualmente com o comando make clean_tables!!!"

clean_tables:
	@rm -rf tables/*

