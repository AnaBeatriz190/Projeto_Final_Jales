# Projeto_Final_Jales

Instituto Federal de Educação, Ciência e Tecnologia da Paraíba - Campus Picuí<br/>
**Curso:** Tecnologia em Desenvolvimento de Sistemas para Internet<br/>
**Disciplina:** Bando de Dados - I<br/>
**Professor Docente:** Jales Monteiro<br/>
**Integrantes:** Antony Ryan, Ana Beatriz, Anderson Cunha e Gabriel Vinicius<br/> 

# Descrição da aplicação

O principal objetivo desse projeto é a criação de um aplicativo para a solicitação de marmitas para estudantes não contemplados com o edital do refeitório. O aplicativo iniciará com o administrador irá logar, colocando o dia, a quantidade de marmitas disponíveis e irá liberar para os alunos. Os alunos poderão acessar após a abertura e logo fará a sua reserva, pegando em um horário específico. O administrador pode acessar a lista visualizando uma lista com as reservas que foram feitas, as quais estarão organizadas em ordem cronológica. A necessidade do projeto é devido a utilização dos grupos para fazer os envios dos formulários manuais para o envio diário das solicitações, causando problemas em visualizar avisos importantes, sobrecarga na comunicação e possíveis falhas no registro dos pedidos. O software será de simples aplicação em Flask. O sistema contém apenas funcionalidades básicas, desenvolvido a fim de obter uma nota para a matéria de Banco de Dados - I do 3° período de Tecnologia em Sistemas para Internet do IFPB - Campus Picuí.

# Modelagens

Conceitual

	Usuário

	ID_Usuário
	Nome
 	Matrícula
	Senha
	Tipo_Usuário(aluno ou admin)
 
	Reserva_Marmita

	ID_Reserva
	ID_Usuário
	Hora_Reserva

	Lista

	ID_Lista
	Quantidade_Disponível
	Data_Lista
	Hora_Liberação

Lógico 

![image](https://github.com/user-attachments/assets/7cb9ee4f-b18c-4257-90b6-7d4761a3d2bf)

