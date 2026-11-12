from scripts.check_osv import high_findings


def report_with_severity(severity: str) -> dict[str, object]:
    return {
        "results": [
            {
                "packages": [
                    {
                        "package": {"name": "example"},
                        "groups": [
                            {
                                "ids": ["OSV-1"],
                                "max_severity": severity,
                            }
                        ],
                    }
                ]
            }
        ]
    }


def test_high_findings_blocks_cvss_seven_and_above() -> None:
    assert high_findings(report_with_severity("7.0")) == {("example", "OSV-1")}


def test_high_findings_allows_lower_severity() -> None:
    assert high_findings(report_with_severity("6.9")) == set()
