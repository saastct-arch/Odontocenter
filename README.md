# OdontoCenter

Site proposta da OdontoCenter (Ipatinga-MG): página inicial, 8 páginas de especialidade e política de privacidade.

- `site/` é o site estático publicado pelo Vercel (`vercel.json` aponta `outputDirectory` para `site`).
- Para regenerar as páginas depois de editar o conteúdo: `cd site && python3 build.py`.
- Conteúdo das especialidades: `site/pages.py`. Estrutura da home: `site/main_body.html`. Estilos e scripts: `site/assets/`.
