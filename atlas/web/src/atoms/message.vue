<template>
  <div class="message">
    {{text}}
  </div>
</template>

<script>
export default {
  name: 'Message',
  props: {
    text: {
      type: String,
      required: true,
    },
  },
}
</script>
