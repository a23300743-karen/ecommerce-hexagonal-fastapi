from app.domain.ports.faq_port import FAQPort


class FAQMemoryRepository(FAQPort):

    FAQS = [
        {
            "keywords": ["cancel"],
            "answer": "Puedes cancelar una orden activa desde la seccion Mis compras. Al cancelarla, las unidades regresan al inventario."
        },
        {
            "keywords": ["pag", "tarjeta", "metodo"],
            "answer": "Actualmente la tienda registra la compra al finalizar el carrito. La integracion con pagos bancarios puede agregarse posteriormente."
        },
        {
            "keywords": ["envi", "entrega", "tiempo", "tarda", "lleg"],
            "answer": "El tiempo estimado de envio es de 3 a 5 dias habiles despues de confirmar la orden."
        },
        {
            "keywords": ["horario", "atencion", "soporte", "atienden"],
            "answer": "Nuestro horario de atencion es de lunes a viernes de 9:00 a 18:00."
        },
        {
            "keywords": ["stock", "dispon", "existencia", "producto"],
            "answer": "El catalogo muestra solamente productos activos con existencias. La cantidad disponible aparece en cada producto."
        },
        {
            "keywords": ["orden", "pedido", "estado", "compra", "historial"],
            "answer": "Puedes consultar el estado y detalle de tus pedidos en la seccion Mis compras."
        }
    ]

    def get_answer(self, question: str) -> str | None:
        normalized_question = question.lower()
        for faq in self.FAQS:
            if any(keyword in normalized_question for keyword in faq["keywords"]):
                return faq["answer"]
        return None
