<template>
  <div id="app">
    <h1 class="title">Blockchains</h1>
    <button class="clear" @click="clear()">Clear</button>
    <section class="blocks-container">
      <div class="blocks">
        <Block
          v-for="(block, index) in blockchain"
          :key="index"
          :block-data="block"
          :xhr="xhr"
          @mine="mine($event)"
          @changedata="changedata($event)"
          @changenonce="changenonce($event)"
        >
        </Block>
        <div class="button-container">
          <button class="newblock" @click="newblock()">+</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import Block from "./components/Block";

export default {
  name: "app",
  components: { Block },
  data() {
    return {
      blockchain: [],
      xhr: null,
    };
  },
  methods: {
    mine(index) {
      this.xhr.open("GET", `http://localhost:5000/mine/${index}`);
      this.xhr.send();
    },
    newblock() {
      this.xhr.open("GET", "http://localhost:5000/newblock");
      this.xhr.send();
    },
    changedata(data) {
      let index = data[0];
      let newdata = data[1];
      this.xhr.open(
        "GET",
        `http://localhost:5000/changedata/${index}?data=${newdata}`
      );
      this.xhr.send();
    },
    changenonce(data) {
      let index = data[0];
      let newnonce = data[1];
      this.xhr.open(
        "GET",
        `http://localhost:5000/changenonce/${index}?nonce=${newnonce}`
      );
      this.xhr.send();
    },
    clear() {
      this.xhr.open("GET", "http://localhost:5000/clear");
      this.xhr.send();
    },
  },
  mounted() {
    this.xhr = new XMLHttpRequest();
    this.xhr.open("GET", "http://localhost:5000/chain");
    this.xhr.send();
    this.xhr.onload = () => {
      if (this.xhr.status == 200) {
        this.blockchain = JSON.parse(this.xhr.response).chain;
      }
    };
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Open+Sans:300,400&display=swap");
* {
  font-family: "Open Sans", sans-serif;
  font-size: 1em;
  margin: 0;
  padding: 0;
}
h1.title {
  display: inline;
  font-size: 32px;
}
.blocks-container {
  overflow-x: auto;
}
.blocks {
  display: inline-flex;
  flex-direction: row;
}
.button-container {
  width: 200px;
}
.newblock {
  margin: 0;
  transform: translate(calc(100px - 50%), calc(215px - 50%));
  width: 100px;
  height: 100px;
  border: none;
  outline: none;
  border-radius: 50%;
  font-size: 48px;
  color: white;
  background-color: blue;
}
.newblock:active {
  background-color: rgb(0, 0, 153);
}
.clear {
  display: inline;
  position: relative;
  top: -5px;
  left: 10px;
  padding: 5px;
  border: none;
  border-radius: 5px;
  color: white;
  background-color: blue;
}
.clear:active {
  background-color: rgb(0, 0, 153);
}
</style>
