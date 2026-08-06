"""Pydantic response models for RepoIntel analysis results."""

from pydantic import BaseModel, ConfigDict


class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AnalyzeRequest(BaseModel):
    url: str


class DocumentationMetricsResponse(ResponseModel):
    readme_exists: bool
    readme_size_bytes: int
    readme_line_count: int
    readme_word_count: int
    readme_character_count: int
    heading_count: int
    heading_levels: dict[int, int]
    max_heading_depth: int
    code_block_count: int
    inline_code_count: int
    image_count: int
    table_count: int
    blockquote_count: int
    horizontal_rule_count: int
    list_count: int
    total_link_count: int
    external_link_count: int
    internal_link_count: int
    relative_link_count: int
    badge_count: int
    has_title: bool
    has_description: bool
    has_table_of_contents: bool
    has_installation_section: bool
    has_usage_section: bool
    has_configuration_section: bool
    has_features_section: bool
    has_examples_section: bool
    has_api_section: bool
    has_testing_section: bool
    has_contributing_section: bool
    has_license_section: bool
    has_changelog_section: bool
    has_faq_section: bool
    has_support_section: bool
    has_acknowledgements_section: bool
    has_roadmap_section: bool
    has_docs_directory: bool
    documentation_file_count: int
    has_license_file: bool
    license_file_name: str
    has_changelog_file: bool
    changelog_file_name: str
    has_contributing_file: bool
    contributing_file_name: str
    has_code_of_conduct: bool
    code_of_conduct_file_name: str
    has_security_file: bool
    security_file_name: str
    has_authors_file: bool
    authors_file_name: str
    has_citation_file: bool
    citation_file_name: str
    markdown_file_count: int
    text_document_count: int
    mentions_github_wiki: bool
    contains_html: bool
    contains_mermaid_diagrams: bool
    contains_latex: bool


class StructureMetricsResponse(ResponseModel):
    total_directories: int
    empty_directories: int
    max_directory_depth: int
    average_directory_depth: float
    root_file_count: int
    nested_file_count: int
    largest_directory: str
    largest_directory_file_count: int
    average_files_per_directory: float
    has_src_directory: bool
    has_test_directory: bool
    has_docs_directory: bool
    has_assets_directory: bool
    has_examples_directory: bool
    has_scripts_directory: bool
    has_config_directory: bool
    has_build_directory: bool
    has_dist_directory: bool
    has_bin_directory: bool
    has_lib_directory: bool
    snake_case_directories: int
    camel_case_directories: int
    pascal_case_directories: int
    kebab_case_directories: int
    uppercase_directories: int
    mixed_case_directories: int
    conventional_layout: bool
    monorepo_detected: bool
    has_gitignore: bool
    has_editorconfig: bool
    has_dockerfile: bool
    has_docker_compose: bool
    has_makefile: bool
    has_package_json: bool
    has_package_lock: bool
    has_yarn_lock: bool
    has_pnpm_lock: bool
    has_requirements_txt: bool
    has_pyproject_toml: bool
    has_poetry_lock: bool
    has_pipfile: bool
    has_pipfile_lock: bool
    has_cargo_toml: bool
    has_go_mod: bool
    has_gradle: bool
    has_maven: bool
    file_extensions: dict[str, int]
    directory_file_counts: dict[str, int]
    directory_depths: dict[str, int]


class CodeMetricsResponse(ResponseModel):
    total_source_files: int
    total_source_lines: int
    largest_file_lines: int
    smallest_file_lines: int
    average_lines_per_file: float
    code_lines: int
    blank_lines: int
    comment_lines: int
    code_line_percentage: float
    blank_line_percentage: float
    comment_line_percentage: float
    files_under_100_lines: int
    files_100_to_300_lines: int
    files_300_to_500_lines: int
    files_over_500_lines: int
    files_over_1000_lines: int
    total_classes: int
    total_functions: int
    total_interfaces: int
    total_enums: int
    docstring_count: int
    documentation_comment_blocks: int
    todo_count: int
    fixme_count: int
    hack_count: int
    xxx_count: int
    duplicate_file_names: int
    duplicate_file_name_list: list[str]
    generated_files: int
    minified_files: int
    source_file_extensions: dict[str, int]
    language_file_counts: dict[str, int]
    language_line_counts: dict[str, int]


class DependencyMetricsResponse(ResponseModel):
    has_npm: bool
    has_yarn: bool
    has_pnpm: bool
    has_pip: bool
    has_poetry: bool
    has_cargo: bool
    has_gradle: bool
    has_maven: bool
    has_go_modules: bool
    total_dependencies: int
    production_dependencies: int
    development_dependencies: int
    optional_dependencies: int
    peer_dependencies: int
    has_lock_file: bool
    has_package_lock: bool
    has_yarn_lock: bool
    has_pnpm_lock: bool
    has_poetry_lock: bool
    has_pipfile_lock: bool
    pinned_dependencies: int
    ranged_dependencies: int
    latest_dependencies: int
    multiple_package_managers: bool


class SecurityMetricsResponse(ResponseModel):
    potential_secrets: int
    aws_keys: int
    github_tokens: int
    google_api_keys: int
    private_keys: int
    has_env_file: bool
    has_env_example: bool
    has_security_policy: bool
    lock_file_present: bool
    executable_scripts: int
    gitignore_present: bool
    certificate_files: int
    key_files: int
    eval_usage: int
    exec_usage: int
    shell_execution_usage: int


class ProjectHealthMetricsResponse(ResponseModel):
    has_readme: bool
    has_changelog: bool
    has_code_of_conduct: bool
    has_docs_directory: bool
    has_github_actions: bool
    has_gitlab_ci: bool
    has_circle_ci: bool
    has_travis_ci: bool
    has_dockerfile: bool
    has_docker_compose: bool
    has_tests: bool
    test_directory_count: int
    has_makefile: bool
    has_gitignore: bool
    has_editorconfig: bool
    total_files: int
    total_directories: int


class RepositoryResponse(ResponseModel):
    name: str
    owner: str
    url: str
    folder_tree: list[str]
    languages: dict[str, int]
    technology_stack: dict[str, list[str]]
    total_files: int
    total_lines: int
    documentation_metrics: DocumentationMetricsResponse | None
    structure_metrics: StructureMetricsResponse | None
    code_metrics: CodeMetricsResponse | None
    dependency_metrics: DependencyMetricsResponse | None
    security_metrics: SecurityMetricsResponse | None
    project_health_metrics: ProjectHealthMetricsResponse | None


class FindingResponse(ResponseModel):
    id: str
    category: str
    severity: str
    title: str
    message: str
    recommendation: str


class ProjectClassificationResponse(ResponseModel):
    primary_category: str
    secondary_category: str | None
    confidence: int
    repository_purpose: str
    maturity: str


class DeductionResponse(ResponseModel):
    finding_id: str
    title: str
    points: int


class DomainScoreResponse(ResponseModel):
    name: str
    max_score: int
    current_score: int
    deductions: list[DeductionResponse]


class OverallScoreResponse(ResponseModel):
    documentation: DomainScoreResponse
    structure: DomainScoreResponse
    code: DomainScoreResponse
    dependency: DomainScoreResponse
    security: DomainScoreResponse
    health: DomainScoreResponse
    overall_score: int


class AnalysisResponse(ResponseModel):
    repository: RepositoryResponse
    findings: list[FindingResponse]
    classification: ProjectClassificationResponse
    score: OverallScoreResponse
