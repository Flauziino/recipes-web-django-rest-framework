# Projeto Web Simples Utilizando Django e Django REST Framework
Um projeto simples desenvolvido com Django Web Framework e Django REST Framework, com o objetivo de demonstrar o nível de habilidade. O projeto utiliza Django Web Framework na versão 4.2.11 e Django REST Framework na versão 3.14.0. O foco está na organização das pastas, cobertura de testes (100%), uso de classes baseadas em views e realização do deploy.

Conteúdo Geral do Projeto
O projeto conta com aplicativos para autores, receitas e tags. O aplicativo de tags foi criado exclusivamente para ser associado às receitas, portanto, seus testes estão dentro do mesmo.

O projeto também inclui uma API, que está organizada de forma diferente do projeto acoplado. No projeto acoplado, o aplicativo de receitas é utilizado apenas para visualização, enquanto o aplicativo de autores realiza o CRUD das receitas. Na API, todo o CRUD é realizado no próprio aplicativo de receitas, sendo que o aplicativo de autores serve apenas para exibir os autores.

Dentro do aplicativo de autores, o único modelo utilizado é o de perfil, contendo o nome do autor (OneToOneField para o modelo User do Django) e uma biografia.

No aplicativo de receitas, há dois modelos: categoria, que contém apenas o nome, e receita, que contém título, descrição, slug, tempo de preparação, unidade de tempo de preparação, porções, unidade de porção, passo a passo da preparação da receita, data de criação, data de atualização, status de publicação, capa, categoria (chave estrangeira para o modelo de categoria), autor (chave estrangeira para o modelo User do Django) e tags (ManyToMany para o modelo de tag).

Por fim, o modelo de tags dentro do aplicativo de tags contém apenas um nome e uma slug.

+ ### Dentro do Aplicativo de Autores
Dentro do aplicativo de autores, é possível realizar cadastro, login, logout e criar o perfil. Além disso, há acesso à dashboard (disponível apenas para usuários logados), onde é possível visualizar as receitas próprias, criar novas receitas, editar as receitas ou excluí-las.

Na API, dentro do aplicativo de autores, é possível visualizar apenas a lista de autores, configurada para mostrar apenas os dados do autor logado, e acessar /ME para ver seus próprios dados.

Em ambos os casos, é necessário estar logado no sistema.

+ ### Dentro do Aplicativo de Receitas
Dentro do aplicativo de receitas, é possível visualizar a lista completa de receitas (por página), visualizar uma receita específica selecionada por ID, visualizar a categoria e realizar pesquisas filtrando por conteúdo do título ou da descrição da receita, tudo isso integrado ao front-end.

Na API, dentro do aplicativo de receitas, praticamente todas as operações são realizadas. O viewset se concentra nos métodos GET, POST, PATCH e DELETE. Com GET, é possível ver a lista de todas as receitas e os detalhes de uma receita específica; com POST, é possível criar uma nova receita se o formulário for válido; com PATCH, é possível atualizar apenas o campo desejado, sem precisar atualizar todos os dados; e com DELETE, é possível excluir receitas.

Para acessar os métodos POST, PATCH e DELETE, é necessário estar logado, utilizando JWT.

## Considerações Finais
O sistema fornece uma interface simples e eficiente para as atividades de criação de usuário, login, logout e dashboard, onde é possível visualizar, editar, criar e excluir receitas com facilidade.

Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir um pull request ou relatar problemas ao abrir uma issue.
##
Autor: Flauziino - Desenvolvedor

