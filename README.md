# API Imóveis - Projeto 2

API RESTful para gerenciamento de imóveis desenvolvida com Flask e MySQL.

## 🚀 Funcionalidades

### Operações CRUD
- ✅ **GET** `/api/v1/imoveis` - Lista todos os imóveis com paginação e filtros
- ✅ **GET** `/api/v1/imoveis/{id}` - Busca um imóvel específico
- ✅ **POST** `/api/v1/imoveis` - Cria um novo imóvel
- ✅ **PUT** `/api/v1/imoveis/{id}` - Atualiza um imóvel existente
- ✅ **DELETE** `/api/v1/imoveis/{id}` - Remove um imóvel

### Filtros e Busca
- ✅ **Por tipo**: `/api/v1/imoveis?tipo=casa`
- ✅ **Por cidade**: `/api/v1/imoveis?cidade=São Paulo`
- ✅ **Combinação**: `/api/v1/imoveis?tipo=apartamento&cidade=Rio de Janeiro`

### Paginação
- ✅ **Página**: `/api/v1/imoveis?page=2`
- ✅ **Itens por página**: `/api/v1/imoveis?per_page=20` (máximo 100)
- ✅ **Combinação**: `/api/v1/imoveis?page=1&per_page=10`

### Ordenação
- ✅ **Por campo**: `/api/v1/imoveis?sort=valor`
- ✅ **Direção**: `/api/v1/imoveis?sort=valor&order=desc`
- ✅ **Campos disponíveis**: `id`, `valor`, `data_aquisicao`, `cidade`, `tipo`

### Documentação
- ✅ **API Docs**: `/api/v1/docs` - Documentação completa da API
- ✅ **Home**: `/` - Informações gerais e links úteis

## 🏗️ Arquitetura

### Nível 3 da Maturidade de Richardson
- ✅ **Controle de versão** da API (`/api/v1/`)
- ✅ **Documentação** integrada
- ✅ **Paginação** com metadados completos
- ✅ **Filtros avançados** e ordenação
- ✅ **Validação** robusta de dados
- ✅ **Códigos HTTP** corretos
- ✅ **HATEOAS** com links de navegação

### Tecnologias
- **Backend**: Flask 3.1.2
- **Banco de dados**: MySQL (Aiven)
- **Testes**: pytest
- **Gerenciamento**: uv

## 📊 Códigos HTTP

| Operação | Sucesso | Erro |
|----------|---------|------|
| GET | 200 | 404 |
| POST | 201 | 400 |
| PUT | 200 | 400, 404 |
| DELETE | 204 | 404 |

## 🧪 Testes

Execute todos os testes:
```bash
uv run pytest test_imoveis.py -v
```

**22 testes** cobrindo:
- ✅ Operações CRUD
- ✅ Filtros e busca
- ✅ Paginação
- ✅ Ordenação
- ✅ Validação de dados
- ✅ Códigos de erro
- ✅ Segurança (SQL injection)

## 🚀 Deploy

**Status**: ⏳ Pendente
- [ ] Deploy na AWS EC2
- [ ] Link da API será adicionado aqui

## 📝 Exemplos de Uso

### Listar imóveis com paginação
```bash
curl "http://localhost:5000/api/v1/imoveis?page=1&per_page=10"
```

### Buscar por tipo e ordenar por valor
```bash
curl "http://localhost:5000/api/v1/imoveis?tipo=casa&sort=valor&order=desc"
```

### Criar novo imóvel
```bash
curl -X POST "http://localhost:5000/api/v1/imoveis" \
  -H "Content-Type: application/json" \
  -d '{
    "logradouro": "Rua das Flores",
    "tipo_logradouro": "Rua",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "cep": "01234-567",
    "tipo": "casa",
    "valor": 500000.00,
    "data_aquisicao": "2023-01-15"
  }'
```

### Documentação da API
```bash
curl "http://localhost:5000/api/v1/docs"
```

## 🎯 Conceito Alcançado

**A+** - Nível 3 da Maturidade de Richardson
- ✅ TDD aplicado corretamente
- ✅ API RESTful completa
- ✅ Banco MySQL (Aiven)
- ✅ Códigos HTTP corretos
- ✅ Paginação e filtros avançados
- ✅ Validação robusta
- ✅ Documentação integrada
- ✅ 22 testes automatizados