<script setup lang="ts">
import {type Ref, ref, watch} from 'vue'

import UiDropdown from "@/components/ui/Dropdown.vue";
import type {ItemCollection} from "@/types/ItemCollection";
import type {Item} from "@/types/Item";

const props = defineProps<{
  type: string,
  title: string,
  refresh: number,
  collection: ItemCollection
}>()

const emit = defineEmits(['selected', 'toggle-color-selector'])

const selected: Ref<Item> = ref(props.collection.getSelected(props.type)) as Ref<Item>;

function openColorSelector(material:string) {
  emit('toggle-color-selector', selected.value, material)
}

async function onSelectionChanged(event:any) {
  if (event.target.value) {
    selected.value = await props.collection.select(event.target.value)
  } else {
    props.collection.unselect(props.type);
    selected.value = props.collection.getSelected(props.type) as Item;
  }
  emit("selected", selected);
}

function getColor(material: any) {
  const c = selected.value.colors.find(selected.value.colors.getCurrent(material))?.palette[2];

  if(!c) {
    return ''
  }

  return `rgb(${c[0]}, ${c[1]}, ${c[2]})`;
}

function isLast(index: number) {
  return index == Object.keys(selected.value.materials).length - 1;
}

function hasNoColors() {
  return !selected.value || !selected.value.id ||
    (Object.keys(selected.value.materials).length == 0 && !selected.value.variants?.length)
}

const VARIANT_CSS: {[key: string]: string} = {
  black: '#1a1a1a', charcoal: '#3c3c3c', shadow: '#4a4a5a', soot: '#2a2a2a',
  gray: '#888', silver: '#bbb', smoke: '#ccc', dove: '#d8d8d8', white: '#f0f0f0',
  ivory: '#fffff0', pearl: '#eee8d5', ice: '#e8f0ff', platinum: '#e5e4e2',
  red: '#cc2222', garnet: '#8b1a1a', wine: '#722f37', maroon: '#800000', ruby: '#9b111e',
  orange: '#e65c00', coral: '#ff6b47', red_orange: '#cc4400', copper: '#b87333',
  yellow: '#ddb800', gold: '#ccaa00', amber: '#ffbf00', lemon: '#fff44f',
  blonde: '#f5deb3', sandy: '#daa520', ginger: '#b5651d',
  green: '#225522', forest: '#228b22', olive: '#6b8e23', fern: '#4f7942',
  mint: '#98ff98', spring: '#00ff7f', emerald: '#50c878', apple: '#8db600',
  blue: '#2244aa', navy: '#001166', sky: '#6699dd', aegean: '#3a7ebf',
  teal: '#008080', cyan: '#00bbcc', cerulean: '#007ba7', denim: '#1560bd',
  azure: '#007fff', royal: '#4169e1', cornflower: '#6495ed', powder: '#b0e0e6',
  purple: '#660066', violet: '#8b00ff', lavender: '#9966cc', amethyst: '#9966cc',
  indigo: '#4b0082', plum: '#8e4585', mauve: '#e0b0ff', heather: '#b086ac',
  pink: '#dd66aa', rose: '#ff007f', cerise: '#de3163',
  brown: '#553311', leather: '#8b5a2b', walnut: '#5c4033', chocolate: '#7b3f00',
  umber: '#635147', sepia: '#704214', tan: '#d2b48c', beige: '#f5f0d7',
  linen: '#faf0e6', peach: '#ffc8a2', apricot: '#fbceb1', salmon: '#fa8072',
  oak: '#806040', ash_brown: '#7d6a57',
  bluegray: '#6a8ba4', slate: '#708090', fog: '#c4c9d4',
  maroon2: '#800000', forest2: '#228b22',
}

function variantSwatchColor(v: string): string {
  return VARIANT_CSS[v] ?? '#777'
}

async function onVariantSelect(variant: string) {
  if (!selected.value) return
  selected.value.setVariant(variant)
  await props.collection.select(selected.value)
  emit('selected', selected)
}

function hasOptions() {
  return Object.keys(getOptions()).length > 0;
}

function getOptions() {
  return props.collection.getFilteredOptions(props.type)
}

async function onSelect(itemId: string) {
  if (itemId) {
    selected.value = await props.collection.select(itemId)
  } else {
    props.collection.unselect(props.type);
    selected.value = props.collection.getSelected(props.type) as Item;
  }

  emit("selected", selected);
}

watch(() => props.refresh, () => {
  selected.value = props.collection.getSelected(props.type) as Item;
})

</script>

<template>
  <div v-if="Object.keys(getOptions()).length > 0">
    <h2 class="text-xs text-zinc-400 font-bold">{{ title }}</h2>
    <div class="flex my-2">
      <ui-dropdown @selected="onSelect" :selected="collection.getSelected(type)" :options="getOptions()" :type="type"
                   :class="{'rounded-r': hasNoColors()}"></ui-dropdown>
      <template v-if="selected">
        <!-- runtime-recolorable items: palette color buttons -->
        <button @click="openColorSelector(key as string)" :title="value.name" class="min-w-8 w-8 bg-zinc-700 p-1"
                :class="{ 'rounded-r': isLast(index) }" v-for="(value, key, index) in selected.materials">
          <div class="h-full rounded align-center" :style="{ backgroundColor: getColor(key)}"></div>
        </button>
        <!-- pre-colored variant items: variant swatch buttons -->
        <template v-if="selected.variants && selected.variants.length > 1">
          <button v-for="(v, i) in selected.variants" :key="v"
                  @click="onVariantSelect(v)" :title="v"
                  class="min-w-5 w-5 p-0.5 bg-zinc-700"
                  :class="{ 'rounded-r': i === selected.variants.length - 1, 'ring-1 ring-amber-400': selected.variant === v }">
            <div class="h-full w-full rounded" :style="{ backgroundColor: variantSwatchColor(v) }"></div>
          </button>
        </template>
      </template>
    </div>

    <div v-if="false" class="flex my-2">
      <select @change="onSelectionChanged($event)"
              class="bg-zinc-700 text-zinc-300 flex-grow p-2 rounded-l truncate w-full"
              :class="{'rounded-r': hasNoColors()}" id="">
        <option value="">Select...</option>
        <option v-for="value in getOptions()" :value="value.id" :selected="value.id == selected.id">{{ value.name }}
        </option>
      </select>

      <template v-if="selected">
        <button @click="openColorSelector(key as string)" :title="value.name" class="min-w-8 w-8 bg-zinc-700 p-1"
                :class="{ 'rounded-r': isLast(index) }" v-for="(value, key, index) in selected.materials">
          <div class="h-full rounded align-center" :style="{ backgroundColor: getColor(key)}"></div>
        </button>
      </template>

    </div>
  </div>
</template>
