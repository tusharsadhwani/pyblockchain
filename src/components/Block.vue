<template>
  <div class="block" :class="{ 'block-valid': blockData.validated }">
    <label for="index" class="label">
      <span>Index</span>
      <input
        name="index"
        class="input"
        type="text"
        :value="blockData.index"
        disabled
      />
    </label>
    <label for="nonce" class="label">
      <span>Nonce</span>
      <input
        name="nonce"
        class="input"
        type="text"
        :value="blockData.nonce"
        @input="changenonce($event, blockData.index)"
      />
    </label>
    <label for="data" class="label">
      <span>Data</span>
      <textarea
        name="data"
        v-model="blockData.data"
        @input="changedata($event, blockData.index)"
        style="resize: none;"
      ></textarea>
    </label>
    <label for="hash" class="label">
      <span>Hash</span>
      <input
        name="hash"
        class="input"
        type="text"
        :value="blockData.hash"
        disabled
      />
    </label>
    <label for="prevhash" class="label">
      <span>Previous Hash</span>
      <input
        name="prevhash"
        class="input"
        type="text"
        :value="blockData.previous_hash"
        disabled
      />
    </label>
    <label for="mine">
      <button
        name="mine"
        :class="{ 'button-valid': blockData.validated }"
        @click="mine(blockData.index)"
      >
        Mine
      </button>
    </label>
  </div>
</template>

<script>
export default {
  props: ["blockData", "xhr"],
  methods: {
    mine(index) {
      this.$emit("mine", index);
    },
    changedata(event, index) {
      this.$emit("changedata", [index, event.target.value]);
    },
    changenonce(event, index) {
      this.$emit("changenonce", [index, event.target.value]);
    },
  },
};
</script>

<style scoped>
.block {
  width: 400px;
  margin: 10px;
  padding: 15px 15px;
  background-color: rgb(255, 112, 112);
  border-radius: 5px;
}
.block-valid {
  background-color: rgb(112, 191, 255);
}
.input {
  width: 65%;
}
.label {
  padding: 5px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
textarea {
  width: 65%;
  height: 200px;
}
button {
  margin-top: 15px;
  padding: 5px;
  width: 80px;
  border: none;
  border-radius: 5px;
  background-color: red;
  color: white;
}
button:active {
  background-color: rgb(153, 0, 0);
}
.button-valid {
  background-color: blue;
}
.button-valid:active {
  background-color: rgb(0, 0, 153);
}
</style>
