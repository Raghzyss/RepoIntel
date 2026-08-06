from dataclasses import dataclass, field


@dataclass
class Deduction:

    finding_id: str

    title: str

    points: int


@dataclass
class DomainScore:

    name: str

    max_score: int

    current_score: int

    deductions: list[Deduction] = field(
        default_factory=list,
    )

    def deduct(
        self,
        points: int,
        finding_id: str,
        title: str,
    ) -> None:

        self.current_score = max(
            0,
            self.current_score - points,
        )

        self.deductions.append(
            Deduction(
                finding_id=finding_id,
                title=title,
                points=points,
            )
        )