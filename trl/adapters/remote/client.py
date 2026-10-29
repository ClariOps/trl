import requests

from trl.core.base import RemoteModuleClient, Report
from trl.core.context import RunContext
from trl.core.ir import (
    DeploymentIR,
    ServiceIR,
    IngressIR,
    ConfigMapIR,
    SecretIR,
    PVCIR,
)


IR_MAPPING = {
    "DeploymentIR": DeploymentIR,
    "ServiceIR": ServiceIR,
    "IngressIR": IngressIR,
    "ConfigMapIR": ConfigMapIR,
    "SecretIR": SecretIR,
    "PVCIR": PVCIR,
}


def _serialize_irs(irs):
    return [
        {
            "kind": ir.kind,
            "manifest": ir.to_manifest(),
        }
        for ir in irs
    ]


def _deserialize_irs(items):
    irs = []

    for item in items:
        kind = item["kind"]
        manifest = item["manifest"]

        ir_class = IR_MAPPING.get(kind)

        if ir_class is None:
            raise ValueError(
                f"Unsupported remote IR type: {kind}"
            )

        irs.append(
            ir_class(manifest=manifest)
        )

    return irs


class HTTPModuleClient(RemoteModuleClient):

    def __init__(
        self,
        name: str,
        endpoint: str,
        timeout: int = 30,
    ):
        self.name = name
        self.endpoint = endpoint
        self.timeout = timeout

    def process(self, ctx: RunContext) -> None:

        payload = {
            "irs": _serialize_irs(ctx.irs),
            "opts": ctx.opts,
            "report": ctx.report.to_dict(),
        }


        response = requests.post(
            self.endpoint,
            json=payload,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()
    
        ctx.irs = _deserialize_irs(
            data["irs"]
        )
        ctx.report = Report.from_dict(data.get("report", {}))