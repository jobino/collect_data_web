from bs4 import BeautifulSoup
import urllib3
from more_itertools import unique_everseen
from collections import OrderedDict
from selenium import webdriver

def get_content_html(page_formated,tag,class_tag,value_class):
  div_datas = page_formated.find_all(tag, {class_tag: value_class})
  get_error = page_formated.find("td", {"id": "mensagemRetorno"})
  if get_error:
    div_datas = False
  return div_datas

def get_crawler_processes(page_formated):
  div_datas = get_content_html(page_formated,"div","class","")
  if div_datas:
    for table_data in div_datas:
      span_datas = table_data.find_all("table", {"class": "secaoFormBody"})
      for span_data in span_datas:
        span_data_values = span_data.find_all("span", {"class": ""})
        list_datas = verify_space(span_data_values)
    spanArea = get_value_tag(span_data,"span","labelClass",'Área: ')
    list_datas.append(spanArea)
    return list_datas
  else:
    return False

def get_crawler_parts_processes(page_formated):
  div_datas = get_content_html(page_formated,"table","id","tablePartesPrincipais")
  if div_datas:
    for dat in div_datas:
      datas = dat.find_all("td", {"align": "left"})
    lista = []
    for ld in datas:
      lista.append(ld.text.strip())
    return lista
  else:
    return False

def get_crawler_move(page_formated):
  div_datas = get_content_html(page_formated,"tbody","id","tabelaUltimasMovimentacoes")
  if div_datas:
    move_describe = []
    move_date = []
    move_list = dict()
    for table_data in div_datas:
      td_datas = table_data.find_all("td")
    move_date,move_describe = add_date_move_list(td_datas,move_date,move_describe)
    move_list = zip(move_date,move_describe)
    return move_list
  else:
    return False

def add_date_move_list(td_datas,move_date,move_describe):
  for i in range(len(td_datas)):
    if(td_datas[i].text.isspace() != True):
      if td_datas[i].text.strip()[0].isdigit():
        move_date.append(td_datas[i].text.strip())
      else:
        move_describe.append(td_datas[i].text.strip())
  return move_date,move_describe

def get_url(urlSite):
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  http = urllib3.PoolManager()
  try:
    page_data = http.request('GET', urlSite)
    page_formated = BeautifulSoup(page_data.data, "lxml")
    return page_formated
  except:
    print("Error URL")

def verify_space(data_value):
  list_datas = []
  for span_data_value in data_value:
    if(span_data_value.text.isspace() != True):
      list_datas.append(span_data_value.text.strip())
  list_datas = list(unique_everseen(list_datas))
  return list_datas

def get_crawler_list(courts,url):
	page_formated = get_url(url)
	datas_processes = get_crawler_processes(page_formated)
	datas_parts = get_crawler_parts_processes(page_formated)
	datas_move = get_crawler_move(page_formated)
	if (datas_processes and datas_parts and datas_move):
		datas = set_dict(courts,[datas_processes,datas_parts])
		return datas, datas_move
	else:
		return "Não existem informações disponíveis para os parâmetros informados.",""

def crawler_concatenate_link(courts,first_link, second_link, third_link, processes):
  processes = str(processes)
  tjms_link_full = first_link + processes[:-5] + second_link + processes + third_link
  return_list = get_crawler_list(courts,tjms_link_full)
  return return_list

def set_dict(courts,data_list):
  data_processes, alls_keys = put_key(courts)
  for i in range(len(alls_keys)):
    data_processes[alls_keys[i]] = dict(zip(data_processes[alls_keys[i]], data_list[i]))
  return data_processes

def put_key(courts):
  data_processes = OrderedDict()
  if courts == "SP":
    data_processes['Dados do Processo']  = ['Processo','Classe','Assunto','Outros Assuntos','Distribuicao','Descricao','Controle','Juiz','Valor da Acao','Área']
  else:
    data_processes['Dados do Processo']  = ['Processo','Classe','Assunto','Distribuicao','Descricao','Controle','Juiz','Valor da Acao','Área']
  data_processes['Partes do Processo'] = ['Autora','Réu']

  keys = ['Dados do Processo','Partes do Processo']
  return data_processes,keys

def get_value_tag(html, tag, value_class, specific_content):
  data_values = html.find(tag, {"class": value_class})
  data_values = data_values.parent.text.strip()
  data_values = data_values.replace(specific_content, '')
  return data_values