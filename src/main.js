const API_BASE_URL = "http://127.0.0.1:8000";

const categoriaSelect = document.getElementById("categoria");
const bloqueProductos = document.getElementById("bloque-productos");
const bloquePedidos = document.getElementById("bloque-pedidos");
const clienteSelect = document.getElementById("cliente");
const resultadoPre = document.getElementById("resultado");

let clientesCargados = false;

categoriaSelect.addEventListener("change", async () => {
    const valor = categoriaSelect.value;

    bloqueProductos.classList.add("hidden");
    bloquePedidos.classList.add("hidden");
    resultadoPre.textContent = "— sin consultas aún —";

    if (valor === "productos") {
        bloqueProductos.classList.remove("hidden");
    } else if (valor === "pedidos") {
        bloquePedidos.classList.remove("hidden");
        if (!clientesCargados) {
            await cargarClientes();
        }
    }
});

async function cargarClientes() {
    try {
        const resp = await fetch(`${API_BASE_URL}/clientes`);
        const clientes = await resp.json();

        console.log('clientes response', clientes)

        clienteSelect.innerHTML = "";
        const optionDefault = document.createElement("option");
        optionDefault.value = "";
        optionDefault.textContent = "— selecciona un cliente —";
        clienteSelect.appendChild(optionDefault);

        clientes.forEach(c => {
            const opt = document.createElement("option");
            opt.value = c;
            opt.textContent = c;
            clienteSelect.appendChild(opt);
        });

        clientesCargados = true;
    } catch (err) {
        clienteSelect.innerHTML = '<option value="">error cargando clientes</option>';
        console.error(err);
    }
}

document.getElementById("btn-consultar").addEventListener("click", async () => {
    const categoria = categoriaSelect.value;

    if (!categoria) {
        resultadoPre.textContent = "selecciona una categoría primero.";
        return;
    }

    let targetValue = "";

    if (categoria === "productos") {
        targetValue = document.getElementById("target_value").value.trim();
        if (!targetValue) {
            resultadoPre.textContent = "escribe un dato de producto para buscar.";
            return;
        }
    } else if (categoria === "pedidos") {
        targetValue = clienteSelect.value;
        if (!targetValue) {
            resultadoPre.textContent = "selecciona un cliente.";
            return;
        }
    }

    resultadoPre.textContent = "consultando...";

    try {
        const url = `${API_BASE_URL}/consulta/${encodeURIComponent(categoria)}/${encodeURIComponent(targetValue)}`;
        const resp = await fetch(url);
        const data = await resp.json();
        resultadoPre.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        resultadoPre.textContent = "error al consultar la API.";
        console.error(err);
    }
});