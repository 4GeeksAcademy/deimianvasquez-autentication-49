import React, { useEffect } from "react"
import { Navigate } from "react-router-dom"
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const Home = () => {

	const { store, dispatch } = useGlobalReducer()



	// useEffect(() => {
	// 	loadMessage()
	// }, [])

	if (!store.token) {
		return <Navigate to="/login" /> // redirecciona a otra vista
	}


	return (
		<div className="container">

			<div>
				<h1>Hola ¿qué tal? Bienvenido al Inicio de la web </h1>
				<p className="mt-4">Ahora iniciaste sesión </p>
			</div>


		</div>
	);
}; 