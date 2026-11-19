import os


def get_concubine_audit_anchors() -> dict:
    master_sha = os.environ.get(
        "CASTLEBERRY_MASTER_BUNDLE_SHA256",
        "6ccb4c68801eb6c97036ca251c8d47a93e07a7a14ac2a0d82dd2a1437d2faab5",
    ).strip()
    ubi_stress_sha = os.environ.get(
        "CASTLEBERRY_UBI_STRESS_SHA256",
        "71d77af81138df43f11b9b5a437233b9bff0451df44f8c8d6ac7ae1ff7a756f9",
    ).strip()
    return {
        "axiom": "Love over God",
        "master_bundle_sha256": master_sha,
        "ubi_stress_test_sha256": ubi_stress_sha,
        "cml_audit_tag": (
            f'<audit_proof master_bundle_sha256="{master_sha}" '
            f'ubi_stress_sha256="{ubi_stress_sha}" />'
        ),
    }
