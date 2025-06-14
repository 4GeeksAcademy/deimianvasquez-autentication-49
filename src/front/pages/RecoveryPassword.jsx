import { useState } from "react"
import { Link } from "react-router-dom"



export const RecoveryPassword = () => {

    const [email, setEmail] = useState("")

    const handleSubmit = async (event) => {
        event.preventDefault()

        if (!email) {
            alert("Por favor ingrese un correo valido")
            return
        }
        const url = import.meta.env.VITE_BACKEND_URL;


        const response = await fetch(`${url}/reset-password`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(email)

        })
        if (response.ok) {
            alert("Se envio un email de restauración de la contraseña")
        }

    }


    return (
        <div className="container">
            <div className="row justify-content-center">
                <h2 className="text-center my-3">recuperrar contraseña :)</h2>
                <div className="col-12 col-md-6" >
                    <form
                        className="border m-2 p-3"
                        onSubmit={handleSubmit}
                    >
                        <div className="form-group mb-3">
                            <label htmlFor="btnEmail">Correo electronico: </label>
                            <input
                                type="text"
                                placeholder="eldeimian@email.com"
                                className="form-control"
                                id="btnEmail"
                                name="email"
                                onChange={(event) => setEmail(event.target.value)}
                                value={email}
                            />
                        </div>

                        <button
                            className="btn btn-outline-primary w-100"
                        >Enviar link de recuperación</button>
                    </form>
                </div>

                <div className="w-100"></div>

                <div className="col-12 col-md-6  d-flex justify-content-between my-1 px-4 ">
                    <Link to="/register">Registrarme</Link>
                    <Link to="/recovery-password">Olvidaste tu contraseña ?</Link>
                </div>
            </div>
        </div>
    )
}