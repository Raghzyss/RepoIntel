from dataclasses import dataclass, field


@dataclass(slots=True)
class DocumentationMetrics:
    """
    Stores deterministic documentation metrics extracted from a repository.

    This class contains only measurable values.
    It does not contain scores, findings, or recommendations.
    """

    # README
    readme_exists: bool = False
    readme_path: str = ""
    readme_size_bytes: int = 0
    readme_line_count: int = 0
    readme_word_count: int = 0
    readme_character_count: int = 0

    # Headings
    heading_count: int = 0
    heading_levels: dict[int, int] = field(default_factory=dict)
    max_heading_depth: int = 0

    # Markdown Elements
    code_block_count: int = 0
    inline_code_count: int = 0
    image_count: int = 0
    table_count: int = 0
    blockquote_count: int = 0
    horizontal_rule_count: int = 0
    list_count: int = 0

    # Links
    total_link_count: int = 0
    external_link_count: int = 0
    internal_link_count: int = 0
    relative_link_count: int = 0

    # Badges
    badge_count: int = 0

    # Documentation Sections
    has_title: bool = False
    has_description: bool = False
    has_table_of_contents: bool = False
    has_installation_section: bool = False
    has_usage_section: bool = False
    has_configuration_section: bool = False
    has_features_section: bool = False
    has_examples_section: bool = False
    has_api_section: bool = False
    has_testing_section: bool = False
    has_contributing_section: bool = False
    has_license_section: bool = False
    has_changelog_section: bool = False
    has_faq_section: bool = False
    has_support_section: bool = False
    has_acknowledgements_section: bool = False
    has_roadmap_section: bool = False

    # Repository Documentation Files
    has_docs_directory: bool = False
    documentation_file_count: int = 0

    has_license_file: bool = False
    license_file_name: str = ""

    has_changelog_file: bool = False
    changelog_file_name: str = ""

    has_contributing_file: bool = False
    contributing_file_name: str = ""

    has_code_of_conduct: bool = False
    code_of_conduct_file_name: str = ""

    has_security_file: bool = False
    security_file_name: str = ""

    has_authors_file: bool = False
    authors_file_name: str = ""

    has_citation_file: bool = False
    citation_file_name: str = ""

    # Documentation Coverage
    markdown_file_count: int = 0
    text_document_count: int = 0

    # Repository Wiki
    mentions_github_wiki: bool = False

    # Miscellaneous
    contains_html: bool = False
    contains_mermaid_diagrams: bool = False
    contains_latex: bool = False