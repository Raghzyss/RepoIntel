from pathlib import Path
import tempfile

from git import Repo

from models.repository import Repository
from core.collector.validator import is_valid_github_url
from core.collector.scanner import RepositoryScanner
from core.collector.language_detector import LanguageDetector
from core.collector.technology_detector import TechnologyDetector


class RepositoryCollector:

    def __init__(self):
        self.temp_dir = Path(__file__).resolve().parents[2] / "temp"
        self.temp_dir.mkdir(exist_ok=True)
        self.workspace_path: Path | None = None

    def collect(self, repo_url: str) -> Repository:

        if not is_valid_github_url(repo_url):
            raise ValueError("Invalid GitHub repository URL.")

        repo_name = repo_url.rstrip("/").split("/")[-1]
        owner = repo_url.rstrip("/").split("/")[-2]

        self.workspace_path = Path(tempfile.mkdtemp(dir=self.temp_dir))
        clone_path = self.workspace_path

        Repo.clone_from(repo_url, clone_path)

        repository = Repository(
            name=repo_name,
            owner=owner,
            url=repo_url,
            local_path=clone_path,
        )

        # Scan repository
        scanner = RepositoryScanner()
        repository = scanner.scan(repository)

        # Detect programming languages
        language_detector = LanguageDetector()
        repository = language_detector.detect(repository)

        # Detect technology stack
        technology_detector = TechnologyDetector()
        repository = technology_detector.detect(repository)

        return repository
