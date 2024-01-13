all:
	@echo "Digite make run para executar o programa"
	@echo "Digite make clean para limpar os arquivos gerados"
	@echo "Digite make clean_tables para limpar as tabelas de input"

run:
	@echo "Digite o número de vezes que cada sentença se repete:"
	@python3 comparator.py > Results/log.txt

clean:
	@rm -rf Results/*
	@echo "!!! não esqueça de apagar as tabelas manualmente com o comando make clean_tables!!!"

clean_tables:
	@rm -rf tables/*

