<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { CharacterCollection } from "@/types/CharacterCollection";
import { CharacterRenderer } from "@/services/CharacterRenderer";
import UiButton from "@/components/ui/Button.vue";
import SideBar from "@/components/ui/SideBar.vue";

const props = defineProps<{
  collection: CharacterCollection,
  renderer: CharacterRenderer
}>();

interface RacePreset {
  id: string;
  name: string;
  description: string;
  data: any; 
}

const races = ref<RacePreset[]>([]);
const selectedRace = ref<RacePreset | null>(null);

onMounted(() => {
  const stored = localStorage.getItem('race-presets');
  if (stored) {
    races.value = JSON.parse(stored);
  } else {
    races.value = [
      { id: 'human-male', name: 'Human Male', description: 'Default human male', data: {"anatomy.body.male": {"colors": {"primary": "ivory"}}} },
      { id: 'human-female', name: 'Human Female', description: 'Default human female', data: {"anatomy.body.female": {"colors": {"primary": "ivory"}}} }
    ];
    saveRaces();
  }
});

const saveRaces = () => {
  localStorage.setItem('race-presets', JSON.stringify(races.value));
};

const addRace = () => {
  const newRace: RacePreset = {
    id: 'race-' + Date.now(),
    name: 'New Race',
    description: '',
    data: props.collection.dumpSelected()
  };
  races.value.push(newRace);
  selectedRace.value = newRace;
  saveRaces();
};

const deleteRace = (id: string) => {
  if (!confirm('Are you sure you want to delete this race?')) return;
  races.value = races.value.filter(r => r.id !== id);
  if (selectedRace.value?.id === id) selectedRace.value = null;
  saveRaces();
};

const updateRace = () => {
    if (selectedRace.value) {
        selectedRace.value.data = props.collection.dumpSelected();
        saveRaces();
        alert('Race preset updated with current character selections!');
    }
}

const applyRace = async (race: RacePreset) => {
  await props.collection.initSelected(race.data);
  props.renderer.draw();
};
</script>

<template>
  <section class="flex flex-1 overflow-hidden relative bg-zinc-900 divide-x divide-zinc-800">
    <side-bar class="w-80">
      <div class="p-4 flex flex-col gap-4">
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-bold text-zinc-200">Race Presets</h2>
          <ui-button @click="addRace" ui="primary" icon="plus" title="Add Race">Add</ui-button>
        </div>
        
        <div class="flex flex-col gap-2">
          <div v-for="race in races" :key="race.id" 
               @click="selectedRace = race"
               class="p-3 rounded cursor-pointer transition-colors"
               :class="{'bg-zinc-700 text-white': selectedRace?.id === race.id, 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700': selectedRace?.id !== race.id}">
            <div class="font-bold">{{ race.name }}</div>
            <div class="text-xs opacity-70 truncate">{{ race.description || 'No description' }}</div>
          </div>
        </div>
      </div>
    </side-bar>

    <main class="flex-1 bg-zinc-800 p-8 overflow-y-auto">
      <div v-if="selectedRace" class="max-w-2xl mx-auto flex flex-col gap-6">
        <div class="flex flex-col gap-2">
          <label class="text-zinc-400 text-sm uppercase font-bold">Race Name</label>
          <input v-model="selectedRace.name" @change="saveRaces" class="bg-zinc-700 text-white p-3 rounded border border-zinc-600 focus:border-amber-500 outline-none">
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-zinc-400 text-sm uppercase font-bold">Description</label>
          <textarea v-model="selectedRace.description" @change="saveRaces" rows="3" class="bg-zinc-700 text-white p-3 rounded border border-zinc-600 focus:border-amber-500 outline-none resize-none"></textarea>
        </div>

        <div class="bg-zinc-900 p-6 rounded-lg border border-zinc-700 flex flex-col gap-4">
            <h3 class="text-zinc-200 font-bold border-b border-zinc-700 pb-2">Actions</h3>
            <div class="grid grid-cols-2 gap-4">
                <ui-button @click="applyRace(selectedRace)" ui="primary" class="w-full h-12" icon="check" title="Apply Preset">Apply Preset</ui-button>
                <ui-button @click="updateRace" ui="secondary" class="w-full h-12" icon="content-save" title="Update from Character">Update from Character</ui-button>
            </div>
            <ui-button @click="deleteRace(selectedRace.id)" ui="danger" class="w-full mt-4" icon="delete" title="Delete Race">Delete Race</ui-button>
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-zinc-400 text-sm uppercase font-bold">Data (JSON)</label>
          <pre class="bg-black text-green-400 p-4 rounded text-xs overflow-auto max-h-64">{{ JSON.stringify(selectedRace.data, null, 2) }}</pre>
        </div>
      </div>
      
      <div v-else class="h-full flex flex-col items-center justify-center text-zinc-500 gap-4">
        <i class="mdi mdi-account-group text-6xl opacity-20"></i>
        <p>Select a race preset from the sidebar or create a new one.</p>
      </div>
    </main>
  </section>
</template>
