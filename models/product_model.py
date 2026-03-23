from dataclasses import dataclass
from datetime import date
from typing import Mapping, Optional


@dataclass(frozen=True)
class ProductModel:
    nome: str
    quantidade: int
    data_validade: date
    id: Optional[int] = None

    @classmethod
    def from_row(cls, row: Mapping[str, object]) -> "ProductModel":
        return cls(
            id=int(row["id"]),
            nome=str(row["nome"]),
            quantidade=int(row["quantidade"]),
            data_validade=date.fromisoformat(str(row["data_validade"])),
        )

    def to_record(self) -> dict[str, object]:
        return {
            "id": self.id,
            "nome": self.nome,
            "quantidade": self.quantidade,
            "data_validade": self.data_validade.isoformat(),
        }

    def status(self, dias_alerta: int, referencia: Optional[date] = None) -> str:
        hoje = referencia or date.today()
        diff = (self.data_validade - hoje).days
        if diff < 0:
            return "vencido"
        if diff == 0:
            return "vence_hoje"
        if diff <= dias_alerta:
            return "vencendo"
        return "ok"

    def to_dict(self, dias_alerta: Optional[int] = None, referencia: Optional[date] = None) -> dict[str, object]:
        produto = self.to_record()
        if dias_alerta is not None:
            produto["status"] = self.status(dias_alerta, referencia)
        return produto