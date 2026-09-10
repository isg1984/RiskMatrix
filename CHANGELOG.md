# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/), e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [2.9.1] - 2026-09-08

### Added
- Interface com dois inputs independentes para upload de arquivos
- Integração com SheetJS bundled localmente (resolveu falha silenciosa de CDN)
- Documentação completa no README.md
- CHANGELOG estruturado

### Fixed
- Bug de corrupção de Excel (duplicate `<selection>` elements em freeze panes)
- Referências de fórmulas quebradas no "slim output mode"

### Changed
- Refinamento dos keywords discriminantes (coluna G)
- Melhor tratamento de exclusion terms (coluna H)

---

## [2.8.0] - 2026-08-15

### Fixed
- Performance: eliminada recalculação redundante de tokens (~50× speedup)
- Otimização de memória em processamento de grandes matrizes

### Changed
- Ajustes na calibração de TF-IDF weights
- Melhor logging de etapas de processamento

---

## [2.7.0] - 2026-08-01

### Fixed
- Corrupção de arquivos Excel ao reapplicar freeze panes
- Validação de input mais robusta

### Added
- Novo modo "slim output" para matrizes maiores
- Mensagens de erro mais descritivas

---

## [2.0.0] - 2026-01-01

### Initial Release
- MVP com cruzamento automático de riscos
- Engine NLP baseado em TF-IDF
- Interface web em Flask
- Output em Excel com anotações
- Suporte a COSO ERM e ISO 31000

---

## [Unreleased]

### Planned
- Suporte a múltiplos formatos de entrada (CSV, JSON)
- Dashboard interativo em tempo real
- API REST para integração com sistemas externos
- Exportação em PDF e Power BI
