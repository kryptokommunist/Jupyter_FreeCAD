"use strict";

var _jupyterThreejs = require("jupyter-threejs");

function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && Symbol.iterator in Object(iter)) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _get(target, property, receiver) { if (typeof Reflect !== "undefined" && Reflect.get) { _get = Reflect.get; } else { _get = function _get(target, property, receiver) { var base = _superPropBase(target, property); if (!base) return; var desc = Object.getOwnPropertyDescriptor(base, property); if (desc.get) { return desc.get.call(receiver); } return desc.value; }; } return _get(target, property, receiver || target); }

function _superPropBase(object, property) { while (!Object.prototype.hasOwnProperty.call(object, property)) { object = _getPrototypeOf(object); if (object === null) break; } return object; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = _getPrototypeOf(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = _getPrototypeOf(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return _possibleConstructorReturn(this, result); }; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Date.prototype.toString.call(Reflect.construct(Date, [], function () {})); return true; } catch (e) { return false; } }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

var widgets = require('@jupyter-widgets/base');

var _ = require('lodash'); // Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
// 
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.
// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
// Custom View. Renders the widget model.


var FirstModel = widgets.DOMWidgetModel.extend({
  defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
    _model_name: 'FirstModel',
    _view_name: 'FirstView',
    _model_module: 'first-widget',
    _view_module: 'first-widget',
    _model_module_version: '^0.1.0',
    _view_module_version: '^0.1.0',
    value: 'Hello World'
  })
});
var FirstView = widgets.DOMWidgetView.extend({
  callback: function callback(inputEvent, formElement) {
    this.model.set({
      'value': formElement[0].value
    }); // update the JS model with the current view value

    this.touch(); // sync the JS model with the Python backend
  },
  render: function render() {
    this.model.on('change:value', this.value_changed, this);
    var view = this; // standard HTML DOM change from JS

    var f = document.createElement("form");
    var i = document.createElement("input"); // input element, text            

    i.setAttribute('type', "text");
    f.appendChild(i);
    this.el.appendChild(f);
    var title = document.createElement("h3");
    this.el.appendChild(title); // initializing the form and the title values  

    i.setAttribute('value', this.model.get('value'));
    title.textContent = this.model.get('value'); // Listening to changes in the frontend input

    f.addEventListener("input", function (inputEvent) {
      return view.callback(inputEvent, f);
    }, false); // handle to access the DOM elements directly

    this.input = i;
    this.title = title;
  },
  value_changed: function value_changed() {
    // access to the 'input' DOM element
    this.input.setAttribute('value', this.model.get('value')); // access to the 'h3' DOM element

    this.title.textContent = this.model.get('value');
  }
});

var THREE = require("three");

var atomGeometry = new THREE.SphereBufferGeometry(0.2, 16, 8);
var atomMaterials = [new THREE.MeshLambertMaterial({
  color: 'red'
}), new THREE.MeshLambertMaterial({
  color: 'green'
}), new THREE.MeshLambertMaterial({
  color: 'yellow'
}), new THREE.MeshLambertMaterial({
  color: 'blue'
}), new THREE.MeshLambertMaterial({
  color: 'cyan'
})];

var CubicLatticeModel = /*#__PURE__*/function (_BlackboxModel) {
  _inherits(CubicLatticeModel, _BlackboxModel);

  var _super = _createSuper(CubicLatticeModel);

  function CubicLatticeModel() {
    _classCallCheck(this, CubicLatticeModel);

    return _super.apply(this, arguments);
  }

  _createClass(CubicLatticeModel, [{
    key: "defaults",
    value: function defaults() {
      return _objectSpread(_objectSpread({}, _get(_getPrototypeOf(CubicLatticeModel.prototype), "defaults", this).call(this)), {
        _model_name: 'CubicLatticeModel',
        _model_module: 'my_module_name',
        basis: [[0, 0, 0]],
        repetitions: [5, 5, 5]
      });
    } // This method is called to create the three.js object of the model:

  }, {
    key: "constructThreeObject",
    value: function constructThreeObject() {
      var root = new THREE.Group(); // Create the children of this group:
      // This is the part that is specific to this example

      this.createLattice(root);
      return root;
    } // This method is called whenever the model changes:

  }, {
    key: "onChange",
    value: function onChange(model, options) {
      _get(_getPrototypeOf(CubicLatticeModel.prototype), "onChange", this).call(this, model, options); // If any of the parameters change, simply rebuild children:


      this.createLattice();
    } // Our custom method to build the lattice:

  }, {
    key: "createLattice",
    value: function createLattice(obj) {
      var _obj, _obj2;

      obj = obj || this.obj; // Set up the basis to tile:

      var basisInput = this.get('basis');
      var basis = new THREE.Group();

      for (var i = 0; i < basisInput.length; ++i) {
        var mesh = new THREE.Mesh(atomGeometry, atomMaterials[i]);
        mesh.position.fromArray(basisInput[i]);
        basis.add(mesh);
      } // Tile in x, y, z:


      var _this$get = this.get('repetitions'),
          _this$get2 = _slicedToArray(_this$get, 3),
          nx = _this$get2[0],
          ny = _this$get2[1],
          nz = _this$get2[2];

      var children = [];

      for (var x = 0; x < nx; ++x) {
        for (var y = 0; y < ny; ++y) {
          for (var z = 0; z < nz; ++z) {
            var copy = basis.clone();
            copy.position.set(x, y, z);
            children.push(copy);
          }
        }
      }

      (_obj = obj).remove.apply(_obj, _toConsumableArray(obj.children));

      (_obj2 = obj).add.apply(_obj2, children);
    }
  }]);

  return CubicLatticeModel;
}(_jupyterThreejs.BlackboxModel);

module.exports = {
  CubicLatticeModel: CubicLatticeModel,
  FirstModel: FirstModel,
  FirstView: FirstView
};
