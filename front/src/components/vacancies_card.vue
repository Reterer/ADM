<template>
    <link href="https://fonts.googleapis.com/css?family=Inter&display=swap" rel="stylesheet">
    <div class=card>
        <div v-html="desc"></div>
    </div>
    <div class="debug">
        <!-- {{ raw_text }} -->
    </div>
</template>

<script>

export default {
    data() {
        return {
        }
    },
    props: {
        raw_text: String,
        desc: String,
    },
}
</script>

<style scoped>
.debug {
    float: left;
    display: block;
}

.card {
    font-size: 12px;
    text-align: left;
    padding: 10px;
    float: left;
    display: block;
    width: 300px;
    height: 500px;
    background-color: rgba(255, 255, 255, 1);
    border-top-left-radius: 30px;
    border-top-right-radius: 30px;
    border-bottom-left-radius: 30px;
    border-bottom-right-radius: 30px;
}
</style>