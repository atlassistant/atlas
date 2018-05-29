<template>
  <div class="execution">
    <div class="execution__header">
      <content-wrapper>
        <tab-container>
          <tab :to="{ name: 'skills' }" icon="build" count="0" text="Skills" />
          <tab :to="{ name: 'settings' }" icon="settings" count="100" text="Settings" />
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
  name: 'Execution',
  components: {
    Tab,
    TabContainer,
    ContentWrapper,
  },
}
</script>


<style lang="scss">
@import "./../_vars.scss";

.execution {
  &__header {
    background-color: color(background);
    border-bottom: 1px solid color(divider);
  }
}

</style>

