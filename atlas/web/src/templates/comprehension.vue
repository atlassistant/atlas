<template>
  <div class="comprehension">
    <div class="comprehension__header">
      <content-wrapper>
        <tab-container>
          <tab :to="{ name: 'intents' }" icon="forum" count="0" text="Intents" />
          <tab :to="{ name: 'entities' }" icon="toys" count="100" text="Entities" />
        </tab-container>
      </content-wrapper>
    </div>

    <router-view />
  </div>
</template>

<script>
import {
  Tab,
  TabContainer,
  ContentWrapper,
} from './../atoms';

export default {
  name: 'Comprehension',
  components: {
    Tab,
    TabContainer,
    ContentWrapper,
  },
}
</script>


<style lang="scss">
@import "./../_vars.scss";

.comprehension {

  &__header {
    background-color: color(background);
    border-bottom: 1px solid color(divider);
  }
}

</style>

