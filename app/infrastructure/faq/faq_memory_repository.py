from app.domain.ports.faq_port import FAQPort


class FAQMemoryRepository(FAQPort):

    FAQS = [
        {
            "keywords": ["orden", "pedido", "estado", "compra"],
            "answer": "Puedes consultar tus ordenes en /orders/. Si tienes el id, revisa /orders/{id}."
        },
        {
            "keywords": ["pago", "pagos", "tarjeta", "metodos"],
            "answer": "Por ahora aceptamos pagos registrados por el sistema. La integracion con pasarela de pago puede agregarse como adapter externo."
        },
        {
            "keywords": ["envio", "entrega", "tiempo", "tarda"],
            "answer": "El tiempo estimado de envio es de 3 a 5 dias habiles despues de confirmar la orden."
        },
        {
            "keywords": ["horario", "atencion", "soporte"],
            "answer": "Nuestro horario de atencion es de lunes a viernes de 9:00 a 18:00."
        },
        {
            "keywords": ["cancelar", "cancelacion"],
            "answer": "Puedes cancelar una orden desde PATCH /orders/{id}/cancel si la orden existe y no ha sido cancelada antes."
        },
        {
            "keywords": ["stock", "disponible", "existencia"],
            "answer": "Puedes revisar productos disponibles desde GET /products/ o buscar por nombre con GET /products/search?name=..."
        }
    ]

    def get_answer(self, question: str) -> str | None:
        normalized_question = question.lower()

        for faq in self.FAQS:
            if any(keyword in normalized_question for keyword in faq["keywords"]):
                return faq["answer"]

        return None
