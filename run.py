"""Punto de entrada: ejecuta este archivo para arrancar MediTrack."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True solo para desarrollo; apágalo al entregar el proyecto.
    app.run(debug=True)
