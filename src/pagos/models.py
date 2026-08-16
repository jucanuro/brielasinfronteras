# App "pagos": vacía a propósito (ver PROMPT.md, sección "Formularios").
#
# En esta version, contacto.Contacto solo registra la intencion de donar; no
# se integra ninguna pasarela de pago todavia. Esta app deja lista la
# interfaz que las futuras integraciones (Culqi/Yape para Peru, PayPal/Stripe
# para el exterior) deberan implementar, sin ningun modelo de base de datos
# ni migracion por ahora.

from abc import ABC, abstractmethod


class PasarelaDePago(ABC):
    """Interfaz que implementará cada pasarela cuando se integre.

    No integrar pasarelas reales todavía (ver PROMPT.md). Referencia para la
    fase futura que conecte esta interfaz con contacto.Contacto.
    """

    @abstractmethod
    def crear_intento_de_pago(self, *, monto, moneda, contacto_id):
        """Inicia un cobro y devuelve la información necesaria para
        completarlo (URL de checkout, token, etc.)."""
        raise NotImplementedError

    @abstractmethod
    def confirmar_pago(self, *, referencia_externa):
        """Verifica el estado de un pago iniciado previamente."""
        raise NotImplementedError
