import streamlit as st
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer,Date
import pandas as pd

if 'login' not in st.session_state:
    st.session_state['login'] = False
if 'cadastrar' not in st.session_state:
    st.session_state['cadastrar'] = False
if 'visualizar_banco' not in st.session_state:
    st.session_state['visualizar_banco'] = False
if 'excluir_paciente' not in st.session_state:
    st.session_state['excluir_paciente'] = False
if 'alterar_dados' not in st.session_state:
    st.session_state['alterar_dados'] = False

db = create_engine('sqlite:///meubanco.db')
Session = sessionmaker(bind = db)
session = Session()

Base = declarative_base()

class usuario(Base):
    __tablename__ = 'usuario'

    usuario = Column('Usuario',String(50),nullable=False,primary_key=True)
    senha = Column('Senha',String(50), nullable=False)

    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha

class paciente(Base):
    __tablename__ = 'pacientes'

    id = Column('ID',Integer, primary_key=True, autoincrement=True)
    nome = Column('nome',String(50),nullable=False)
    idade = Column('idade',Integer, nullable= False)
    data_nascimento = Column('data_nascimento', Date, nullable= False)
    ocupacao = Column('ocupação', String(50), nullable=False)
    endereco = Column('endereço', String(100), nullable=False)
    cpf = Column('cpf', String(50), unique=True, nullable=False)
    telefone = Column('telefone', String(50), unique=True, nullable=False)

    def __init__(self,nome , idade, data_nascimento, ocupacao, endereco, cpf, telefone):
        self.nome = nome
        self.idade = idade
        self.data_nascimento = data_nascimento
        self.ocupacao = ocupacao
        self.endereco = endereco
        self.cpf = cpf
        self.telefone = telefone

Base.metadata.create_all(bind=db)

def login():
    login = st.container(border=True)
    login.markdown("""
    <h2 style='text-align: center;'>Login</h2>
    """, unsafe_allow_html=True)
    login.divider()
    usuario_nome = login.text_input(label='Usuário', placeholder='Digite o usuário')
    senha_usuario = login.text_input(label='Senha', type='password', placeholder='Digite a senha')
    usuario_existente = session.query(usuario).filter(usuario.usuario == usuario_nome).first()
    senha_existente =  session.query(usuario).filter(usuario.senha == senha_usuario).first()
    col1, col2, col3 = login.columns([3,1,3])
    with login:
        if col2.button(label='Logar'):
            if usuario_existente == None or senha_existente == None:
                 st.error('Usuário ou senha Incorretos')
            else:
                st.success('Acesso permitido')
                st.session_state['login'] = True


def registrar_usuario():
    registro = st.container(border=True)
    usuario_registro = registro.text_input('Digite o usuário para registrar')
    senha_registro = registro.text_input('Digite a senha de registro', type='password')
    if registro.button('Confirmar Registro'):
        dados_registro = usuario(usuario=usuario_registro,senha=senha_registro)
        session.add(dados_registro)
        session.commit()
        st.success('Usuário Registrado')
        st.rerun()
    

def pagina_principal():
    st.title('Página Principal')
    col1, col2 = st.columns(2,border=True,vertical_alignment='center')
    if col1.button('Cadastrar Paciente', key ='Cadastro'):
        st.session_state['cadastrar'] = True

    if col1.button('Alterar Dados do Paciente'):
        st.session_state['alterar_dados'] = True

    if col2.button('Excluir Paciente'):
        st.session_state['excluir_paciente'] = True

    if col2.button('Visualizar Banco de Dados'):
        st.session_state['visualizar_banco'] = True
    
    if st.button('Voltar para a página de login', key='voltar_login'):
        st.session_state['login'] = False
        st.rerun()

def cadastro_paciente():
    cadastro = st.container(border=True)
    cadastro.text("Cadastro Paciente:")
    nome_paciente = cadastro.text_input('Nome do Paciente', placeholder='Digite o nome do paciente')
    idade_paciente = cadastro.text_input('Idade',placeholder='Digite a idade do paciente')
    ano_nascimento_paciente = cadastro.date_input('Data de Nascimento:')
    ocupacao_paciente = cadastro.text_input('Ocupação:', placeholder='Digite a ocupação do paciente')
    endereco_paciente = cadastro.text_input('Endereço', placeholder='Digite o endereço do paciente')
    cpf_paciente = cadastro.text_input('CPF:', placeholder='Digite o CPF do paciente')
    telefone_paciente = cadastro.text_input('Telefone:', placeholder= 'Digite o telefone do paciente')

    if cadastro.button("Enviar Dados"):
        st.success('Dados Cadastrados')
        usuario = paciente(nome=nome_paciente,idade=idade_paciente,data_nascimento=ano_nascimento_paciente,ocupacao=ocupacao_paciente,endereco=endereco_paciente,cpf=cpf_paciente,telefone=telefone_paciente)
        session.add(usuario)
        session.commit()
    if st.button('pagina principal'):
        st.session_state['cadastrar'] = False
        st.rerun()

def alterar_paciente():
    alterar_dados = st.container(border=True)
    id_alterar = int(alterar_dados.number_input('Digite o ID', min_value=1))
    paciente_existente = session.query(paciente).filter(paciente.id == id_alterar).first()
    if paciente_existente == None:
        st.error('O paciente não existe, digite o ID novamente')
    else:
        usuario_alterar = session.query(paciente).filter_by(id=id_alterar).first()

        dados_paciente = {
            'ID' : usuario_alterar.id,
            'Nome' : usuario_alterar.nome,
            'Idade' : usuario_alterar.idade,
            'Data de Nascimento' : usuario_alterar.data_nascimento,
            'Ocupação' : usuario_alterar.ocupacao,
            'Endereço' : usuario_alterar.endereco,
            'CPF' : usuario_alterar.cpf,
            'Telefone' : usuario_alterar.telefone
        }

        alterar_dados.text('Dados do paciente:')
        df = pd.DataFrame([dados_paciente])
        alterar_dados.dataframe(df)

        colunas = ['Nome',
                'Idade',
               'Data de Nascimento',
               'Ocupação',
               'Endereço',
               'CPF',
               'Telefone']
    
        opcoes = alterar_dados.multiselect('Selecione a informação que será alterado', colunas)
    
        if opcoes == ['Nome']:
            alterar_nome = alterar_dados.text_input('Digite aqui:')
            if alterar_dados.button('Confirmar'):
                usuario_alterar.nome = alterar_nome
                session.add(usuario_alterar)
                session.commit()
                st.success('Nome alterado')

        elif opcoes == ['Idade']:
            alterar_idade = alterar_dados.number_input('Digite aqui:', min_value=0)
            if(alterar_dados.button('Confirmar')):
                usuario_alterar.idade = alterar_idade
                session.add(usuario_alterar)
                session.commit()
                st.success('Idade alterada')

        elif opcoes == ['Data de Nascimento']:
            alterar_data_nascimento = alterar_dados.date_input('Digite aqui:')
            if alterar_dados.button('Confirmar'):
                usuario_alterar.data_nascimento = alterar_data_nascimento
                session.add(usuario_alterar)
                session.commit()
                st.success('Data de Nascimento alterada')

        elif opcoes == ['Ocupação']:
            alterar_ocupacao = alterar_dados.text_input('Digite aqui:')
            if alterar_dados.button('Confirmar'):
                usuario_alterar.ocupacao = alterar_ocupacao
                session.add(usuario_alterar)
                session.commit()
                st.success('Ocupação alterada')

        elif opcoes == ['Endereço']:
            alterar_endereco = alterar_dados.text_input('Digite aqui:')
            if alterar_dados.button('Confirmar'):
                usuario_alterar.endereco = alterar_endereco
                session.add(usuario_alterar)
                session.commit()
                st.success('Endereço alterado')

        elif opcoes == ['CPF']:
            alterar_cpf = alterar_dados.text_input('Digite aqui:')
            if alterar_dados.button('Confirmar'):
                usuario_alterar.cpf = alterar_cpf
                session.add(usuario_alterar)
                session.commit()
                st.success('CPF alterado')

        elif opcoes == ['Telefone']:
            alterar_telefone = alterar_dados.text_input('Digite aqui:')
            if alterar_dados.button('Confirmar'):
                usuario_alterar.telefone = alterar_telefone
                session.add(usuario_alterar)
                session.commit()
                st.success('Telefone alterado')

    if st.button('Voltar para a página principal'):
        st.session_state['alterar_dados'] = False

def excluir_paciente():
    form_excluir = st.container(border=True)
    paciente_id = int(form_excluir.number_input('Digite o ID', min_value=1))
    paciente_existente = session.query(paciente).filter(paciente.id == paciente_id).first()

    if form_excluir.button('Ver dados do paciente'):
        if paciente_existente == None:
            st.error('O paciente não existe, digite o ID novamente')
        else:
            paciente_escolhido = session.query(paciente).filter_by(id=paciente_id).first()
            data = {'ID' : paciente_escolhido.id,
                'Nome' : paciente_escolhido.nome,
                'Idade' : paciente_escolhido.idade,
                'Data de Nascimento' : paciente_escolhido.data_nascimento,
                'Ocupação' : paciente_escolhido.ocupacao,
                'Endereço' : paciente_escolhido.endereco,
                'CPF' : paciente_escolhido.cpf,
                'Telefone' : paciente_escolhido.telefone} 
            df = pd.DataFrame([data])
            form_excluir.table(df)
        
    if form_excluir.button('Confirmar Exclusão'):
        if paciente_existente == None:
            st.error('O paciente não existe, digite o ID novamente')
        else:
            session.delete(paciente_existente)
            session.commit()
            st.success('Paciente Excluído')
        
                

    if st.button('Voltar para a página principal'):
        st.session_state['excluir_paciente'] = False
        st.rerun()
    
def visualizar_banco():
    st.title('Tabela')
    pacientes = session.query(paciente).all()

    if not pacientes:
        st.warning('Nenhum paciente cadastrado')
    else:
        dataframe = [{
            'ID' : p.id,
            'Nome' : p.nome,
            'Idade' : p.idade,
            'data de nascimento' : p.data_nascimento,
            'ocupação' : p.ocupacao,
            'endereço' : p.endereco,
            'CPF' : p.cpf,
            'telefone' : p.telefone
        } for p in pacientes]

        df = pd.DataFrame(dataframe)

        st.dataframe(df)

    if st.button('Voltar para a página principal'):
        st.session_state['visualizar_banco'] = False
        st.rerun()



usuarios_cadastrados = session.query(usuario).all()
if not usuarios_cadastrados:
    registrar_usuario()
else:
    if st.session_state['login']:
        if st.session_state['cadastrar']:
            cadastro_paciente()
        elif st.session_state['visualizar_banco']:
            visualizar_banco()
        elif st.session_state['excluir_paciente']:
            excluir_paciente()
        elif st.session_state['alterar_dados']:
            alterar_paciente()
        else:
            pagina_principal()
    else:
        login()

    

    
    