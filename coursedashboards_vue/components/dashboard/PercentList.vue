<template>
    <div>
        <TransitionGroup name="list" tag="ul">
            <li v-for="item in itemsToBeDisplayed" :key="item">
                <span v-if="item.percent < 1">&lt;1% </span>
                <span v-else>{{ Math.round(item.percent) }}% </span>
                {{ item.title }}
            </li>
        </TransitionGroup>
        <button v-if="length < items.length" class="btn btn-small btn-primary" @click="viewAll">View all</button>
        <button v-else-if="length == items.length && length > 5" class="btn btn-small btn-primary"
            @click="viewLess">View less</button>
    </div>
</template>

<script>
export default {
    name: "PercentList",
    components: {
    },
    props: {
        items: Array,
    },
    data() {
        return {
            length: 5,
        };
    },
    computed: {
        itemsToBeDisplayed() {
            return this.items.slice(0, this.length);
        }
    },
    methods: {
        viewAll() {
            this.length = this.items.length;
        },
        viewLess() {
            this.length = 5;
        },
    },
    created: function () {
    },
};
</script>

<style scoped>
ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
}

.list-enter-active,
.list-leave-active {
    transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
    opacity: 0;
    transform: translateX(30px);
}
</style>
