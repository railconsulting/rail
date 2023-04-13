/** @odoo-module **/

import OrderSummary from 'point_of_sale.OrderSummary';
import Registries from 'point_of_sale.Registries';

export const OrderSummaryPricelist = (OrderSummary) =>
    class OrderSummaryPricelist extends OrderSummary {
        getTotalQty() {
            return this.props.order.total_qty;
        }
    };

Registries.Component.extend(OrderSummary, OrderSummaryPricelist)
