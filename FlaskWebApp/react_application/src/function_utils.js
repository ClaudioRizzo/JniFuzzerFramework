export const TAG_FILTER = 'tag_filter';

export let API;

if (process.env.NODE_ENV === 'production'){
    API = 'https://10.212.237.98:12345/api';
} else {
    API = 'https://127.0.0.1:12345/api';
}


/**
 * Load a state from local storage.
 * 
 * This function trys to load a state from local storage. In case
 * no state is found, `undefined` is returned (and the  state will be 
 * loaded as it was never saved).
 * 
 * @returns {*} state
 */
export const loadState = () => {
    try {
        const serializedState = localStorage.getItem('state');
        if(serializedState === null) {
            return undefined;
        }
        console.log(JSON.parse(serializedState))
        return JSON.parse(serializedState);
    } catch(err) {
        return undefined;
    }
};

/**
 * This method takes a serializable state and saves it
 * to local storage. After it is saved, you can re-load it by using
 * `loadState` function.
 * 
 * @param {*} state a serializable state to be saved
 */
export const saveState = (state) => {
    try {
        const serializedState = JSON.stringify(state);
        localStorage.setItem('state', serializedState);
    } catch(err) {
        console.log(err)
    }
}

/**
 * Check if the given key is in the local store or not.
 * 
 * @param {*} key the key we want to check to be in the local store
 * @returns {bool} true if the key is found
 */
export const isInLocalStore = (key) => {
    return localStorage.getItem(key) !== null
}

export const getFromLocalStore = (key) => {
    try {
        const serialized = localStorage.getItem(key);
        if(serialized === null) {
            return undefined;
        }
        return JSON.parse(serialized);

    } catch {
        return undefined;
    }
    
}

export const removeFromLocalStore = (key) => {
    localStorage.removeItem(key);
}

/**
 * Add a `json serializable` object to the localstore
 * 
 * @param {*} key 
 * @param {*} value 
 */
export const addToLocalStore = (key, value) => {
    try {
        const serialized = JSON.stringify(value);
        localStorage.setItem(key, serialized);
    } catch(err) {
        console.log(err)
    }
}

export const addTagFilter = (color) => {
    let colors = getFromLocalStore(TAG_FILTER)
    if(colors === undefined) colors = [];
    colors.push(color);
    addToLocalStore(TAG_FILTER, colors);
}

export const removeTagFilter = (color) => {
    let colors = getFromLocalStore(TAG_FILTER);
    if(colors !== undefined) {
        let index = colors.indexOf(color);
        
        if(index !== -1) {
            colors.splice(index, 1);
            addToLocalStore(TAG_FILTER, colors);
        }
        
        if(colors.length <= 0) {
            // we completely get rid of the filter if 
            // no colors are present
            removeFromLocalStore(TAG_FILTER);
        }
    } 
}

export const isColorInFilter = (color) => {
    let colors = getFromLocalStore(TAG_FILTER);
    if(colors === undefined){
        colors = [];
    }
    // console.log(color +" | " +colors.find((element) => color === element))
    return undefined !== colors.find((element) => color === element);
}

/**
 * Filter a list of apks by tag color.
 * 
 * The method checks the local storage for the colors to filter by.
 * If the no color is found (`TAG_FILTER` is not a key of the local store),
 * then the original list is return, meaning no filter is active.
 * 
 * **NOTE**: each apk in `apk_list` must have a tags property.
 * 
 * @param {*} apk_list list of apks object to be filtered.
 * @returns {*} filtered list of apks.
 */
export const filterByTag = (apk_list) => {
    if(isInLocalStore(TAG_FILTER)){
        let colors = getFromLocalStore(TAG_FILTER);
        
        return apk_list.filter(apk => {
           let tags = apk.tags;
           let filtered_tags = tags.filter(tag => (colors.includes(tag.color) && tag.active))
           return filtered_tags.length > 0;
        });
    } else {
        return apk_list;
    }
}
