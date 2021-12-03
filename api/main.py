import re
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pymongo import MongoClient

def init():

	# Nome da pasta de leitura dos arquivos
	pastaIN = 'C:/Users/Paulo/Ubiquiti UniFi/logs/remote'
	# local para salvar o arquivo final (inicialmente como txt)
	fileOUT = open('media/LogUsersOut.txt','w')
	tagsOUT = open('media/Tags.txt','w')

	# Classe de usuários
	class users:
		def __init__(self, index, uap, mac, time, status):
			self.index = 'User'+ ' '+ str(index)		
			self.uap = uap
			self.mac = mac
			self.time = time
			self.status = status
	'''
	
	'''
	# Função que exibe todos os Associateds
	def shownUsersAssociated(user):

		def Uap2Tag_str(lista, mac_uap):

			name_re = re.compile(r'u\'name\':')
			member_re = re.compile(r'u\'member_table\':')
			tag = ''

			for i in range(len(lista)):
				try:
					name = name_re.search(lista[i])[0]
					member = member_re.search(lista[i])[0]
					a = lista[i].index(name)
					b = lista[i].index(member)
					tagg = (lista[i][a+11:b-3])
					#print(tagg)
					for x in (lista[i][b+18:-3]).split(', '):
						mac_replace = (x.replace('u','').strip('\''))
						mac_replace = mac_replace.replace(':','')
						if (mac_uap == mac_replace):
							tag = tagg
							return tag

				except: return ''

			return ''

		client = MongoClient('localhost', 27117)
		dbs = client.list_database_names()
		#print('Bancos de dados:\n', dbs)
		db = client['ace']
		colls = db.list_collection_names()
		#print('\nTabelas:\n',colls)
		coll = db['tag']
		all_colls = coll.find()

		list_cursor = list(all_colls)
		#print('\nConteúdo dentro de \'tag\':\n',lista)

		for i in range(len(list_cursor)):
			tagsOUT.write(str(list_cursor[i]))

		tagsOUT.close()

		lista = list(open('C:/Users/Paulo/Documents/Faculdade/TCC2/API/Tags.txt'))

		#fileOUT.write("---- Nº de Usuarios Associados por UAP ----")
		nUser = []
		uapAux = 0
		tag = []
		use = []
		lenUap = []

		for u in user:
			if ((conect.search(u.status)) and (len(u.status) <= 10)):
				if (u.uap != uapAux):
					i=1
					uapAux = u.uap
					use = u.uap[u.uap.find(',')+1:]
					t = Uap2Tag_str(lista, use)
					if (t != ''): tag.append(t)
				lenUap.append(len(tag))
		
		if (tag != []):

			nMax = max(lenUap)

			for i in range(nMax+1):			
				nUser.append(lenUap.count(i))
			nUser.pop(0)
			try:
				i = sum(nUser)

				if (i == 1):
					df = pd.DataFrame(nUser, index=tag, columns=['Usuários'])
					plt.figure(figsize=[int(len(max(tag, key=len))/4)+4,len(tag)+3])
					heatmap = sns.heatmap(df, vmin=0, cmap='YlOrRd', cbar=True, square=True, linewidths=.5, annot=True)#, cbar_kws={'label': 'colorbar title'})
					plt.yticks(rotation=0) 
					plt.title('Total de Usuários: %d'%i, pad=15)
					plt.savefig('media/heatmap.png')

				else:
					df = pd.DataFrame(nUser, index=tag, columns=['Usuários'])
					plt.figure(figsize=[int(len(max(tag, key=len))/4)+2.5,len(tag)+3])
					heatmap = sns.heatmap(df, vmin=0, cmap='YlOrRd', cbar=True, square=True, linewidths=.5, annot=True)#, cbar_kws={'label': 'colorbar title'})
					plt.yticks(rotation=0) 
					plt.title('Total de Usuários: %d'%i, pad=15)
					plt.savefig('media/heatmap.png')
					#plt.show()

				if(len(tag) == len(nUser)):
					j = 0
					for i in range (len(nUser)):
						j += nUser[i]
						#fileOUT.write('\n')
						fileOUT.write(user[j-1].time)
						fileOUT.write('\n')
						fileOUT.write(tag[i])
						fileOUT.write('\n')
						fileOUT.write(str(nUser[i]))
						fileOUT.write('\n')

			except:
				tag = ['None']
				hMap = pd.DataFrame(0, index=tag, columns=['Usuários'])
				heatmap = sns.heatmap(hMap, vmin=0, cmap='YlOrRd', cbar=True, square=True, linewidths=.5, annot=True)#, cbar_kws={'label': 'colorbar title'})
				plt.yticks(rotation=0) 
				plt.title('Total de Usuários: 0', pad=15)
				plt.savefig('media/heatmap.png')

		else:
			plt.switch_backend('agg')
			tag = ['None']
			plt.figure(figsize=[int(len(max(tag, key=len))/4)+4,len(tag)+3])
			df = pd.DataFrame(0, index=tag, columns=['Usuários'])
			heatmap = sns.heatmap(df, vmin=0, cmap='YlOrRd', cbar=True, square=True, linewidths=.5, annot=True)#, cbar_kws={'label': 'colorbar title'})
			plt.yticks(rotation=0) 
			plt.title('Total de Usuários: 0', pad=15)
			fig1 = plt.figure(1)
			plt.savefig('media/heatmap.png')

	'''
	
	'''
	# Parâmetros que serão passados a classe de usuários
	userHis = []
	user = []
	uap = []
	mac = []
	time = []
	status = []
	uapAux = []
	macAux = []
	i = 0

	# Expressões regulares para encontrar 'associated', 'disassociated','uap','mac' e 'date'
	conect = re.compile(r'associated')
	disconect = re.compile(r'disassociated')
	date = re.compile(r'\d\d:\d\d:\d\d')
	uap_re = re.compile(r'\w+,\w\w\w\w\w\w\w\w\w\w\w\w')
	mac_re = re.compile(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w')

	# Loop que percorre toda a pasta
	for diretorio, subpastas, arquivos in os.walk(pastaIN):
		# Loop que percorre os arquivos
		for arquivo in arquivos:
			# Faz a leitura somente dos arquvos .log
			if arquivo.endswith(".log"):
				# Atribui o arquivo atual como fileIN
				fileIN = open(os.path.join(os.path.realpath(diretorio), arquivo))
				# Loop que percorre todo o arquivo
				for text in fileIN:
					# Loop que define cada linha do arquivo
				    for line in text.split('\n'):
				    	if (len(line) > 100):
				    		# Se 'disassociated' for encontrado na linha
					    	if disconect.search(line):
					    		
					    		# Define os parâmetros pelas posições da linha
					    		uap = uap_re.search(line)[0]
					    		mac = mac_re.search(line)[0]
					    		time = date.search(line)[0]
					    		status = disconect.search(line)[0]

					    		
					    		# Verifica se o UAP já é existente
					    		if (uap != uapAux) or (mac != macAux):
					    			i+=1
					    			macAux = mac
					    			uapAux = uap

					    		for test in user:
					    			if test.mac == mac:
					    				i = int(test.index[5:])

					    		try:
					    			userHis.append(users(i,uap,mac,time,status))
					    			user[i-1] = users(i,uap,mac,time,status)

					    		except:
					    			user.append(users(i,uap,mac,time,status))

					    	# Se 'associated' for encontrado na linha
					    	elif conect.search(line):
					    		#print(line)
					    		uap = uap_re.search(line)[0]
					    		mac = mac_re.search(line)[0]
					    		time = date.search(line)[0]
					    		status = conect.search(line)[0]

					    		
					    		if (uap != uapAux) or (mac != macAux):
					    			i+=1
					    			macAux = mac
					    			uapAux = uap

					    		for test in user:
					    			if test.mac == mac:
					    				i = int(test.index[5:])

					    		try:
					    			userHis.append(users(i,uap,mac,time,status))
					    			user[i-1] = users(i,uap,mac,time,status)

					    		except:
					    			user.append(users(i,uap,mac,time,status))


	# Chama as funções desejadas
	shownUsersAssociated(user)
	# Fecha o arquivo final
	fileOUT.close()