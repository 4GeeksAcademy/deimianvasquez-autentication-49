import React, { useEffect } from "react"
import { Navigate } from "react-router-dom"
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const Home = () => {

	const { store, dispatch } = useGlobalReducer()



	const loadData = async () => {

		const url = import.meta.env.VITE_BACKEND_URL;

		const response = await fetch(`${url}/me`, {
			method: "GET",
			headers: {
				"Authorization": `Bearer ${store.token}`
			}
		})

		const me = await response.json()

		dispatch({ type: "ADD_ME", payload: me })
	}

	useEffect(() => {
		loadData()
	}, [])

	if (!store.token) {
		return <Navigate to="/login" /> // redirecciona a otra vista
	}


	return (
		<div className="container">

			<div>
				<h1>Hola ¿qué tal? Bienvenido al Inicio de la web </h1>
				<p className="mt-4">Ahora iniciaste sesión </p>
				<img src={`${store.me.avatar}`} />
			</div>


		</div>
	);
}; 