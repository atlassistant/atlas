<template>
  <div class="spinner">
    <div class="spinner__bounce"></div>
    <div class="spinner__bounce"></div>
  </div>
</template>

<style lang="scss">
@import "./../_vars.scss";

.spinner {
  width: baseline();
  height: baseline();
  padding: baseline(0.5);
  position: relative;

  &__bounce {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-color: color(brand);
    opacity: 0.6;
    position: absolute;
    top: 0;
    left: 0;
    animation: sk-bounce 2.0s infinite ease-in-out;

    &:last-child {
      animation-delay: -1.0s;
    }
  }

  @keyframes sk-bounce {
      0%, 100% { 
        transform: scale(0.0);
      } 50% { 
        transform: scale(1.0);
      }
    }
}
</style>

