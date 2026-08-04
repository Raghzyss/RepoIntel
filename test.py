from core.collector.collector import RepositoryCollector
from core.extractor.documentation_extractor import DocumentationExtractor
from core.rules.documentation_rules import DocumentationRules

collector = RepositoryCollector()

repo = collector.collect("https://github.com/psf/requests")

repo = DocumentationExtractor().extract(repo)

findings = DocumentationRules().evaluate(
    repo.documentation_metrics
)

for finding in findings:
    print(finding)