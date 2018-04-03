<template>
  <i class="material-icons">{{name}}</i>
</template>

<script>
export default {
  name: 'Icon',
  props: {
    name: {
      type: String,
      required: true,
    },
  },
}
</script>


