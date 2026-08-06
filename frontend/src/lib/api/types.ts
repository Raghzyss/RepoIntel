export interface AnalyzeRequest {
  url: string;
}

export interface DocumentationMetricsResponse {
  readme_exists: boolean;
  readme_size_bytes: number;
  readme_line_count: number;
  readme_word_count: number;
  readme_character_count: number;
  heading_count: number;
  heading_levels: Record<string, number>;
  max_heading_depth: number;
  code_block_count: number;
  inline_code_count: number;
  image_count: number;
  table_count: number;
  blockquote_count: number;
  horizontal_rule_count: number;
  list_count: number;
  total_link_count: number;
  external_link_count: number;
  internal_link_count: number;
  relative_link_count: number;
  badge_count: number;
  has_title: boolean;
  has_description: boolean;
  has_table_of_contents: boolean;
  has_installation_section: boolean;
  has_usage_section: boolean;
  has_configuration_section: boolean;
  has_features_section: boolean;
  has_examples_section: boolean;
  has_api_section: boolean;
  has_testing_section: boolean;
  has_contributing_section: boolean;
  has_license_section: boolean;
  has_changelog_section: boolean;
  has_faq_section: boolean;
  has_support_section: boolean;
  has_acknowledgements_section: boolean;
  has_roadmap_section: boolean;
  has_docs_directory: boolean;
  documentation_file_count: number;
  has_license_file: boolean;
  license_file_name: string;
  has_changelog_file: boolean;
  changelog_file_name: string;
  has_contributing_file: boolean;
  contributing_file_name: string;
  has_code_of_conduct: boolean;
  code_of_conduct_file_name: string;
  has_security_file: boolean;
  security_file_name: string;
  has_authors_file: boolean;
  authors_file_name: string;
  has_citation_file: boolean;
  citation_file_name: string;
  markdown_file_count: number;
  text_document_count: number;
  mentions_github_wiki: boolean;
  contains_html: boolean;
  contains_mermaid_diagrams: boolean;
  contains_latex: boolean;
}

export interface StructureMetricsResponse {
  total_directories: number;
  empty_directories: number;
  max_directory_depth: number;
  average_directory_depth: number;
  root_file_count: number;
  nested_file_count: number;
  largest_directory: string;
  largest_directory_file_count: number;
  average_files_per_directory: number;
  has_src_directory: boolean;
  has_test_directory: boolean;
  has_docs_directory: boolean;
  has_assets_directory: boolean;
  has_examples_directory: boolean;
  has_scripts_directory: boolean;
  has_config_directory: boolean;
  has_build_directory: boolean;
  has_dist_directory: boolean;
  has_bin_directory: boolean;
  has_lib_directory: boolean;
  snake_case_directories: number;
  camel_case_directories: number;
  pascal_case_directories: number;
  kebab_case_directories: number;
  uppercase_directories: number;
  mixed_case_directories: number;
  conventional_layout: boolean;
  monorepo_detected: boolean;
  has_gitignore: boolean;
  has_editorconfig: boolean;
  has_dockerfile: boolean;
  has_docker_compose: boolean;
  has_makefile: boolean;
  has_package_json: boolean;
  has_package_lock: boolean;
  has_yarn_lock: boolean;
  has_pnpm_lock: boolean;
  has_requirements_txt: boolean;
  has_pyproject_toml: boolean;
  has_poetry_lock: boolean;
  has_pipfile: boolean;
  has_pipfile_lock: boolean;
  has_cargo_toml: boolean;
  has_go_mod: boolean;
  has_gradle: boolean;
  has_maven: boolean;
  file_extensions: Record<string, number>;
  directory_file_counts: Record<string, number>;
  directory_depths: Record<string, number>;
}

export interface CodeMetricsResponse {
  total_source_files: number;
  total_source_lines: number;
  largest_file_lines: number;
  smallest_file_lines: number;
  average_lines_per_file: number;
  code_lines: number;
  blank_lines: number;
  comment_lines: number;
  code_line_percentage: number;
  blank_line_percentage: number;
  comment_line_percentage: number;
  files_under_100_lines: number;
  files_100_to_300_lines: number;
  files_300_to_500_lines: number;
  files_over_500_lines: number;
  files_over_1000_lines: number;
  total_classes: number;
  total_functions: number;
  total_interfaces: number;
  total_enums: number;
  docstring_count: number;
  documentation_comment_blocks: number;
  todo_count: number;
  fixme_count: number;
  hack_count: number;
  xxx_count: number;
  duplicate_file_names: number;
  duplicate_file_name_list: string[];
  generated_files: number;
  minified_files: number;
  source_file_extensions: Record<string, number>;
  language_file_counts: Record<string, number>;
  language_line_counts: Record<string, number>;
}

export interface DependencyMetricsResponse {
  has_npm: boolean;
  has_yarn: boolean;
  has_pnpm: boolean;
  has_pip: boolean;
  has_poetry: boolean;
  has_cargo: boolean;
  has_gradle: boolean;
  has_maven: boolean;
  has_go_modules: boolean;
  total_dependencies: number;
  production_dependencies: number;
  development_dependencies: number;
  optional_dependencies: number;
  peer_dependencies: number;
  has_lock_file: boolean;
  has_package_lock: boolean;
  has_yarn_lock: boolean;
  has_pnpm_lock: boolean;
  has_poetry_lock: boolean;
  has_pipfile_lock: boolean;
  pinned_dependencies: number;
  ranged_dependencies: number;
  latest_dependencies: number;
  multiple_package_managers: boolean;
}

export interface SecurityMetricsResponse {
  potential_secrets: number;
  aws_keys: number;
  github_tokens: number;
  google_api_keys: number;
  private_keys: number;
  has_env_file: boolean;
  has_env_example: boolean;
  has_security_policy: boolean;
  lock_file_present: boolean;
  executable_scripts: number;
  gitignore_present: boolean;
  certificate_files: number;
  key_files: number;
  eval_usage: number;
  exec_usage: number;
  shell_execution_usage: number;
}

export interface ProjectHealthMetricsResponse {
  has_readme: boolean;
  has_changelog: boolean;
  has_code_of_conduct: boolean;
  has_docs_directory: boolean;
  has_github_actions: boolean;
  has_gitlab_ci: boolean;
  has_circle_ci: boolean;
  has_travis_ci: boolean;
  has_dockerfile: boolean;
  has_docker_compose: boolean;
  has_tests: boolean;
  test_directory_count: number;
  has_makefile: boolean;
  has_gitignore: boolean;
  has_editorconfig: boolean;
  total_files: number;
  total_directories: number;
}

export interface RepositoryResponse {
  name: string;
  owner: string;
  url: string;
  folder_tree: string[];
  languages: Record<string, number>;
  technology_stack: Record<string, string[]>;
  total_files: number;
  total_lines: number;
  documentation_metrics: DocumentationMetricsResponse | null;
  structure_metrics: StructureMetricsResponse | null;
  code_metrics: CodeMetricsResponse | null;
  dependency_metrics: DependencyMetricsResponse | null;
  security_metrics: SecurityMetricsResponse | null;
  project_health_metrics: ProjectHealthMetricsResponse | null;
}

export interface FindingResponse {
  id: string;
  category: string;
  severity: string;
  title: string;
  message: string;
  recommendation: string;
}

export interface ProjectClassificationResponse {
  primary_category: string;
  secondary_category: string | null;
  confidence: number;
  repository_purpose: string;
  maturity: string;
}

export interface DeductionResponse {
  finding_id: string;
  title: string;
  points: number;
}

export interface DomainScoreResponse {
  name: string;
  max_score: number;
  current_score: number;
  deductions: DeductionResponse[];
}

export interface OverallScoreResponse {
  documentation: DomainScoreResponse;
  structure: DomainScoreResponse;
  code: DomainScoreResponse;
  dependency: DomainScoreResponse;
  security: DomainScoreResponse;
  health: DomainScoreResponse;
  overall_score: number;
}

export interface AnalysisResponse {
  repository: RepositoryResponse;
  findings: FindingResponse[];
  classification: ProjectClassificationResponse;
  score: OverallScoreResponse;
}
