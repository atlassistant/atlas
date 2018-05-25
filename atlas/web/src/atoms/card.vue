<template>
  <div class="card">
    <img :src="media" class="card__media" v-if="media" />
    <div class="card__content">
      <h2 class="card__header" v-if="header_link"><a :href="header_link" :alt="header">{{header}}</a></h2>
      <h2 class="card__header" v-else>{{header}}</h2>
      <h3 class="card__subhead" v-if="subhead">{{subhead}}</h3>

      <p class="card__text">{{text}}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    media: String,
    header: {
      type: String,
      required: true,
    },
    header_link: String,
    subhead: String,
    text: {
      type: String,
      required: true,
    },
  },
}
</script>

<style lang="scss">
@import "./../_vars.scss";

.card {
  @include cell($shrink: 0);
  background-color: color(background, 1);
  box-shadow: 0 0 10px color(shadow);
  border: 1px solid color(divider);
  border-radius: $border-radius;
  max-width: 100%;

  &__header {
    @include type(h4);
    padding: baseline();
    padding-bottom: 0;
  }

  &__subhead {
    @include type(h6);
    color: color(text, 1);
    padding: 0 baseline();
  }

  &__text {
    color: color(text, 1);
    padding: baseline();
    padding-top: baseline(0.5);
  }

  &__media {
    max-width: 100%;
    height: auto;
  }

  & + & {
    margin-left: baseline();
  }
}
</style>

