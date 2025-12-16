<script setup></script>

<template>
    <div class="parent">
        <div class="div1">
            <div class="logo">
                <img src="../assets/LOGO_APP.png" alt="Logo T-radar" />
            </div>
        </div>
        <div class="div2">
            <h1>T-Radar</h1>
            <h4 style="color: grey; font-weight: 200;"><i>Gestiona tu presencia</i></h4>
        </div>
    </div>

    <div class="opciones">
        <ul>
        <li><a href="#">Panel</a></li>
        <li><a href="#">Analíticas</a></li>
        <li><a href="#">Audiencia</a></li>
        <li><a href="#">Publicaciones</a></li>
        <li><a href="#">Programar</a></li>
        <li><a href="#">Tendencias</a></li>
        <li><a href="#">Hashtags</a></li>
        <li><a href="#">Notificaciones</a></li>
        <li><a href="#">Crear</a></li>
        <li><a href="#">Configuración</a></li>
        </ul>
    </div>
</template>

<style scoped>
    .parent {
  display: grid;
  grid-template-columns: auto 1fr; /* logo más estrecho, texto más ancho */
  align-items: center;             /* centra verticalmente en ambas columnas */
  column-gap: 12px;
  
}

.div1,
.div2 {
  display: flex;
  align-items: center; /* centra verticalmente dentro de cada celda */
}

.logo img {
  width: 50px;         /* prueba con un tamaño un poco mayor */
  height: auto;
  display: block;
}
.div2 {
  flex-direction: column;
}
.div2 h1,
.div2 h4 {
  margin: 0;
  line-height: 1.2;
}
</style>